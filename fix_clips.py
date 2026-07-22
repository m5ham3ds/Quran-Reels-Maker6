import re

with open('app/src/main/java/com/example/ui/PopularClipsScreen.kt', 'r') as f:
    content = f.read()

target = r"""cachedFiles\?\.forEach \{ it\.delete\(\) \}\s+com\.example\.generator\.SystemDiagnosticTracker\.clearLogs\(\)\s+com\.example\.generator\.SystemDiagnosticTracker\.addLog\("SAMPLE", "بدء جلب عينة المقطع من الرابط: \$\{clip\.audioUrl\}"\)\s+kotlinx\.coroutines\.withContext\(kotlinx\.coroutines\.Dispatchers\.Main\) \{\s+Toast\.makeText\(context, if \(isArabic\) "جاري جلب العينة من المنصة\.\.\." else "Fetching sample from platform\.\.\.", Toast\.LENGTH_SHORT\)\.show\(\)\s+\}\s+val whisperClient = com\.example\.generator\.WhisperXClient\(\)\s+val result = whisperClient\.processAudio\(null, clip\.audioUrl, ""\) \{ progress -> \s+com\.example\.generator\.SystemDiagnosticTracker\.addLog\("SAMPLE_WHISPER", progress\)\s+\}\s+if \(result\.audioUrl\.isNotBlank\(\)\) \{\s+com\.example\.generator\.SystemDiagnosticTracker\.addLog\("SAMPLE", "تم الحصول على رابط الصوت: \$\{result\.audioUrl\}\. جاري التنزيل\.\.\."\)\s+val fixedUrl = if \(result\.audioUrl\.contains\("file="\)\) \{\s+val prefix = "file="\s+val fileIdx = result\.audioUrl\.indexOf\(prefix\)\s+val baseUrl = result\.audioUrl\.substring\(0, fileIdx \+ prefix\.length\)\s+val pathStr = result\.audioUrl\.substring\(fileIdx \+ prefix\.length\)\s+val encodedPath = pathStr\.split\("/"\)\.joinToString\("/"\) \{ segment ->\s+java\.net\.URLEncoder\.encode\(segment, "UTF-8"\)\.replace\("\+", "%20"\)\s+\}\s+baseUrl \+ encodedPath\s+\} else \{\s+result\.audioUrl"""

replacement = """cachedFiles?.forEach { it.delete() }
                                                                
                                                                val prefs = context.getSharedPreferences("SampleUrlsCache", android.content.Context.MODE_PRIVATE)
                                                                val cachedUrl = prefs.getString("url_${safeId}", null)
                                                                val cachedTime = prefs.getLong("time_${safeId}", 0L)
                                                                val tenMinutesAgo = System.currentTimeMillis() - (10 * 60 * 1000)
                                                                
                                                                var targetAudioUrl = ""
                                                                if (cachedUrl != null && cachedTime > tenMinutesAgo) {
                                                                    com.example.generator.SystemDiagnosticTracker.addLog("SAMPLE", "تخطي الاتصال: استخدام رابط عينة محفوظ في ذاكرة التطبيق (صالح لـ 10 دقائق)")
                                                                    targetAudioUrl = cachedUrl
                                                                } else {
                                                                    com.example.generator.SystemDiagnosticTracker.clearLogs()
                                                                    com.example.generator.SystemDiagnosticTracker.addLog("SAMPLE", "بدء جلب عينة المقطع من الرابط: ${clip.audioUrl}")
                                                                    kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                                                        Toast.makeText(context, if (isArabic) "جاري جلب العينة من المنصة..." else "Fetching sample from platform...", Toast.LENGTH_SHORT).show()
                                                                    }
                                                                    val whisperClient = com.example.generator.WhisperXClient()
                                                                    val result = whisperClient.processAudio(null, clip.audioUrl, "") { progress -> 
                                                                        com.example.generator.SystemDiagnosticTracker.addLog("SAMPLE_WHISPER", progress)
                                                                    }
                                                                    targetAudioUrl = result.audioUrl
                                                                    if (targetAudioUrl.isNotBlank()) {
                                                                        prefs.edit()
                                                                            .putString("url_${safeId}", targetAudioUrl)
                                                                            .putLong("time_${safeId}", System.currentTimeMillis())
                                                                            .apply()
                                                                    }
                                                                }
                                                                
                                                                if (targetAudioUrl.isNotBlank()) {
                                                                    com.example.generator.SystemDiagnosticTracker.addLog("SAMPLE", "تم الحصول على رابط الصوت: $targetAudioUrl. جاري التنزيل...")
                                                                       
                                                                    val fixedUrl = if (targetAudioUrl.contains("file=")) {
                                                                        val prefix = "file="
                                                                        val fileIdx = targetAudioUrl.indexOf(prefix)
                                                                        val baseUrl = targetAudioUrl.substring(0, fileIdx + prefix.length)
                                                                        val pathStr = targetAudioUrl.substring(fileIdx + prefix.length)
                                                                        val encodedPath = pathStr.split("/").joinToString("/") { segment ->
                                                                            java.net.URLEncoder.encode(segment, "UTF-8").replace("+", "%20")
                                                                        }
                                                                        baseUrl + encodedPath
                                                                    } else {
                                                                        targetAudioUrl"""

content, count = re.subn(target, replacement, content)
print(f"Replaced {count} occurrences")
with open('app/src/main/java/com/example/ui/PopularClipsScreen.kt', 'w') as f:
    f.write(content)

