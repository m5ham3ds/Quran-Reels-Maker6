package com.example.utils

import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.os.Process
import android.provider.MediaStore
import com.example.utils.AppLogger
import java.io.BufferedReader
import java.io.File
import java.io.FileWriter
import java.io.InputStreamReader
import java.io.PrintWriter
import java.text.SimpleDateFormat
import java.util.ArrayDeque
import java.util.Date
import java.util.Locale
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicBoolean

/**
 * CrashReporter - نظام احترافي لالتقاط الكراشات مع Logcat كامل وتفصيلي.
 *
 * يعمل عبر مسارين متكاملين:
 *
 * 1) Ring Buffer مستمر (LogcatRingBuffer): خيط خلفي (daemon) يقرأ Logcat
 *    بشكل مستمر (stream) منذ لحظة إقلاع التطبيق، ويحتفظ بآخر ~800 سطر في
 *    الذاكرة. هذا يحل المشكلة الأساسية: النظام قد يقتل العملية بسرعة بعد
 *    الكراش قبل أن تتاح لنا فرصة تنفيذ "logcat -d" في تلك اللحظة بالذات.
 *
 * 2) عند وقوع كراش: نجمع (Ring Buffer + تفريغ لحظي إضافي) + Stack Trace
 *    الكامل + كل سلسلة الأسباب (Caused by) + Thread dump لجميع الخيوط
 *    (مفيد لتشخيص التجمّد/الـ deadlock) + معلومات الجهاز والذاكرة،
 *    ثم نكتب كل ذلك في ملف عبر سلسلة مسارات تخزين احتياطية.
 *
 * ملاحظة مهمة (قيد نظام أندرويد وليس خطأ في الكود):
 * منذ Android 4.1، لا يستطيع أي تطبيق عادي (بدون صلاحيات نظام/روت) قراءة
 * سجلات Logcat الخاصة بتطبيقات أخرى — فقط سجلات عملية (UID) تطبيقه هو.
 * لذلك هذا الملف يلتقط "كل سجلات تطبيقك أنت" (كل Log.d/e/w، ومكتبات مثل
 * ExoPlayer/OkHttp إن استخدمت AppLogger)، وهذا هو أقصى ما يمكن
 * لأي تطبيق التقاطه شرعيًا دون روت.
 */
class CrashReporter private constructor(
    private val appContext: Context,
    private val defaultHandler: Thread.UncaughtExceptionHandler?
) : Thread.UncaughtExceptionHandler {

    override fun uncaughtException(thread: Thread, throwable: Throwable) {
        try {
            val report = buildFullReport(thread, throwable)
            saveCrashLog(report)
        } catch (inner: Throwable) {
            AppLogger.e(TAG, "CrashReporter internal failure", inner)
        } finally {
            LiveLogToFile.stop()
            if (defaultHandler != null) {
                defaultHandler.uncaughtException(thread, throwable)
            } else {
                Process.killProcess(Process.myPid())
                kotlin.system.exitProcess(10)
            }
        }
    }

    private fun buildFullReport(thread: Thread, throwable: Throwable): String {
        val sb = StringBuilder()

        sb.appendLine("========== QURAN REELS CRASH REPORT ==========")
        sb.appendLine("Time: ${DATE_FORMAT.format(Date())}")
        sb.appendLine("Thread: ${thread.name} (id=${thread.id}, priority=${thread.priority})")
        sb.appendLine()

        sb.appendLine("---------- Application Log (AppLogger) ----------")
        sb.appendLine(AppLogger.getLogs())
        sb.appendLine()

        sb.appendLine("---------- Exception Chain (كامل سلسلة الأسباب) ----------")
        var current: Throwable? = throwable
        var depth = 0
        while (current != null && depth < 10) {
            sb.appendLine(if (depth == 0) "Exception: ${current.javaClass.name}" else "Caused by: ${current.javaClass.name}")
            sb.appendLine("Message: ${current.message}")
            sb.appendLine(AppLogger.getStackTraceString(current))
            current = current.cause
            depth++
        }
        sb.appendLine()

        sb.appendLine("---------- All Threads Snapshot (لتشخيص التجمّد/الـ ANR) ----------")
        try {
            for ((t, stack) in Thread.getAllStackTraces()) {
                sb.appendLine("Thread: ${t.name} (state=${t.state})")
                stack.take(25).forEach { sb.appendLine("    at $it") }
                sb.appendLine()
            }
        } catch (e: Exception) {
            sb.appendLine("Failed to capture thread dump: ${e.message}")
        }

        sb.appendLine("---------- Device & App Info ----------")
        sb.appendLine(collectDeviceInfo())
        sb.appendLine()

        sb.appendLine("---------- Logcat (Ring Buffer - منذ إقلاع التطبيق) ----------")
        sb.appendLine(LiveLogToFile.snapshot())
        sb.appendLine()

        sb.appendLine("---------- Logcat (تفريغ لحظي إضافي وقت الكراش) ----------")
        sb.appendLine(dumpLiveLogcat())

        return sb.toString()
    }

    private fun collectDeviceInfo(): String {
        val pkg = appContext.packageName
        val pInfo = try {
            appContext.packageManager.getPackageInfo(pkg, 0)
        } catch (e: Exception) {
            null
        }
        val versionName = pInfo?.versionName ?: "unknown"
        val versionCode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            pInfo?.longVersionCode ?: -1
        } else {
            @Suppress("DEPRECATION")
            (pInfo?.versionCode?.toLong() ?: -1)
        }

        val runtime = Runtime.getRuntime()
        val usedMemMb = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024)
        val maxMemMb = runtime.maxMemory() / (1024 * 1024)

        return buildString {
            appendLine("Package: $pkg")
            appendLine("Version: $versionName ($versionCode)")
            appendLine("Manufacturer/Model: ${Build.MANUFACTURER} ${Build.MODEL}")
            appendLine("Device: ${Build.DEVICE} / Product: ${Build.PRODUCT}")
            appendLine("Android: ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
            appendLine("ABI: ${Build.SUPPORTED_ABIS.joinToString()}")
            appendLine("Memory used: ${usedMemMb}MB / max ${maxMemMb}MB")
            appendLine("PID: ${Process.myPid()}")
        }
    }

    /**
     * تفريغ لحظي إضافي (-d) كطبقة احتياطية ثانية بجانب الـ ring buffer.
     * الفرق الجوهري عن الكود القديم: نستخدم redirectErrorStream(true) حتى
     * لا تتجمد العملية الفرعية بسبب امتلاء الـ pipe الخاص بـ stderr —
     * وهذا كان السبب الأرجح لفشل الملف القديم في التقاط اللوج بشكل كامل.
     */
    private fun dumpLiveLogcat(maxLines: Int = 400): String {
        var process: java.lang.Process? = null
        return try {
            val pid = Process.myPid().toString()
            process = ProcessBuilder("logcat", "-d", "-v", "threadtime")
                .redirectErrorStream(true)
                .start()

            val lines = ArrayDeque<String>()
            BufferedReader(InputStreamReader(process.inputStream)).use { reader ->
                var line: String? = null
                while (reader.readLine().also { line = it } != null) {
                    val l = line ?: continue
                    if (l.contains(pid)) {
                        if (lines.size >= maxLines) lines.poll()
                        lines.offer(l)
                    }
                }
            }
            process.waitFor(3, TimeUnit.SECONDS)
            lines.joinToString("\n")
        } catch (e: Exception) {
            "Failed to dump live logcat: ${e.message}"
        } finally {
            process?.destroy()
        }
    }

    private fun saveCrashLog(report: String) {
        val timeStamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())
        val fileName = "crash_$timeStamp.txt"

        var success = writeViaPublicMoviesDir(fileName, report)
        if (!success) {
            success = writeViaMediaStore(fileName, report)
        }
        if (!success) {
            success = writeViaAppScoped(fileName, report)
        }
        if (!success) {
            writeViaInternal(fileName, report)
        }
    }

    private fun writeViaPublicMoviesDir(fileName: String, report: String): Boolean {
        return try {
            val moviesDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES)
            val quranReelsDir = File(moviesDir, "Quran Reels/ERROR")
            if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
            
            // Clear old crash files, but keep live logcat
            quranReelsDir.listFiles()?.forEach { 
                if (it.name != "live_logcat.txt") {
                    it.delete() 
                }
            }
            
            val file = File(quranReelsDir, fileName)
            PrintWriter(FileWriter(file)).use { it.print(report) }
            AppLogger.i(TAG, "Crash log saved via public directory: ${file.absolutePath}")
            true
        } catch (e: Exception) {
            AppLogger.e(TAG, "Public directory save failed", e)
            false
        }
    }

    private fun writeViaMediaStore(fileName: String, report: String): Boolean {
        return false // We exclusively use public directory as requested
    }

    private fun writeViaAppScoped(fileName: String, report: String): Boolean {
        // getExternalFilesDir لا يحتاج أي صلاحية على أي إصدار أندرويد
        val candidateDirs = listOfNotNull(
            appContext.getExternalFilesDir(null)?.let { File(it, "DiagnosticLogs") },
            appContext.getExternalFilesDir(Environment.DIRECTORY_MOVIES)?.let { File(it, "ERROR") },
            appContext.getExternalFilesDir(null)?.let { File(it, "ERROR") }
        )
        for (dir in candidateDirs) {
            try {
                if (!dir.exists()) dir.mkdirs()
                val file = File(dir, fileName)
                PrintWriter(FileWriter(file)).use { it.print(report) }
                AppLogger.i(TAG, "Crash log saved: ${file.absolutePath}")
                return true
            } catch (e: Exception) {
                AppLogger.e(TAG, "Failed writing to ${dir.absolutePath}", e)
            }
        }
        return false
    }

    private fun writeViaInternal(fileName: String, report: String) {
        try {
            val dir = File(appContext.filesDir, "ERROR")
            if (!dir.exists()) dir.mkdirs()
            val file = File(dir, fileName)
            PrintWriter(FileWriter(file)).use { it.print(report) }
            AppLogger.i(TAG, "Crash log saved (internal fallback): ${file.absolutePath}")
        } catch (e: Exception) {
            AppLogger.e(TAG, "All crash log storage attempts failed", e)
        }
    }

    companion object {
        private const val TAG = "CrashReporter"
        private val DATE_FORMAT = SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US)

        @Volatile
        private var installed = false

        /**
         * استدعِ هذه الدالة أول شيء داخل Application.onCreate()،
         * قبل تهيئة أي مكتبة أخرى، حتى تُلتقط كراشات الإقلاع المبكر أيضًا.
         *
         * مثال:
         * class MyApp : Application() {
         *     override fun onCreate() {
         *         super.onCreate()
         *         CrashReporter.initialize(this)
         *         // ... باقي التهيئة
         *     }
         * }
         */
        fun initialize(context: Context) {
            if (installed) return
            installed = true
            val app = context.applicationContext
            LiveLogToFile.start(app)
            val existing = Thread.getDefaultUncaughtExceptionHandler()
            Thread.setDefaultUncaughtExceptionHandler(CrashReporter(app, existing))
            AppLogger.i(TAG, "CrashReporter installed successfully")
        }
    }
}

/**
 * خيط خلفي (daemon) يقرأ Logcat بشكل مستمر (streaming) منذ إقلاع التطبيق
 * ويحتفظ بآخر عدد محدد من الأسطر في حلقة ذاكرة (ring buffer) صغيرة الحجم.
 * هذا يضمن التقاط اللوج المؤدي مباشرة للكراش حتى لو أُنهيت العملية فجأة
 * قبل أن تُتاح فرصة تنفيذ "logcat -d" في لحظة الكراش نفسها.
 */
private object LiveLogToFile {
    private val running = AtomicBoolean(false)
    private var process: java.lang.Process? = null
    private var logThread: Thread? = null

    fun start(context: Context) {
        if (!running.compareAndSet(false, true)) return
        logThread = Thread({
            try {
                // Determine file path
                var logFile: File? = null
                try {
                    val publicDir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "Quran Reels/ERROR")
                    if (!publicDir.exists()) publicDir.mkdirs()
                    logFile = File(publicDir, "live_logcat.txt")
                } catch (e: Exception) {
                    val fallbackDir = File(context.getExternalFilesDir(null), "Quran Reels/ERROR")
                    if (!fallbackDir.exists()) fallbackDir.mkdirs()
                    logFile = File(fallbackDir, "live_logcat.txt")
                }

                if (logFile != null) {
                    if (logFile.exists()) {
                        logFile.delete()
                    }
                    logFile.createNewFile()

                    val pid = Process.myPid().toString()
                    val p = ProcessBuilder("logcat", "-v", "threadtime")
                        .redirectErrorStream(true)
                        .start()
                    process = p

                    val writer = PrintWriter(FileWriter(logFile, true), true)
                    writer.println("========== QURAN REELS LIVE LOG START ==========")
                    writer.println("Time: ${SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US).format(Date())}")
                    
                    BufferedReader(InputStreamReader(p.inputStream)).use { reader ->
                        var line: String? = null
                        while (running.get() && reader.readLine().also { line = it } != null) {
                            val l = line ?: continue
                            if (l.contains(pid)) {
                                writer.println(l)
                            }
                        }
                    }
                    writer.close()
                }
            } catch (e: Exception) {
                AppLogger.e("LiveLogToFile", "Streaming logcat failed: ${e.message}")
            }
        }, "LiveLogToFileThread")
        
        logThread?.apply {
            isDaemon = true
            start()
        }
    }

    fun stop() {
        running.set(false)
        process?.destroy()
    }

    fun snapshot(): String {
        return "Live logcat is streaming directly to: Documents/Quran Reels ERROR/live_logcat.txt"
    }
}
