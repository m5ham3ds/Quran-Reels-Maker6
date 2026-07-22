import re

with open('app/src/main/java/com/example/utils/CrashReporter.kt', 'r') as f:
    content = f.read()

old_crash = """    private fun writeViaPublicMoviesDir(fileName: String, report: String): Boolean {
        return try {
            val moviesDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES)
            val quranReelsDir = File(moviesDir, "Quran Reels/ERROR")
            if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
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
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) return false
        return try {
            val values = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
                put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOCUMENTS + "/Quran Reels ERROR")
            }
            val uri = appContext.contentResolver.insert(
                MediaStore.Files.getContentUri("external"), values
            ) ?: return false
            appContext.contentResolver.openOutputStream(uri)?.use { out ->
                out.write(report.toByteArray())
                out.flush()
            }
            AppLogger.i(TAG, "Crash log saved via MediaStore: $uri")
            true
        } catch (e: Exception) {
            AppLogger.e(TAG, "MediaStore save failed", e)
            false
        }
    }"""

new_crash = """    private fun writeViaPublicMoviesDir(fileName: String, report: String): Boolean {
        return try {
            val moviesDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES)
            val quranReelsDir = File(moviesDir, "Quran Reels/ERROR")
            if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
            
            // Clear old crash files
            quranReelsDir.listFiles()?.forEach { it.delete() }
            
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
    }"""

if old_crash in content:
    content = content.replace(old_crash, new_crash)
    with open('app/src/main/java/com/example/utils/CrashReporter.kt', 'w') as f:
        f.write(content)
    print("Patched CrashReporter successfully")
else:
    print("Could not find old_crash in CrashReporter")

