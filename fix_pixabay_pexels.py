import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    lines = f.readlines()

new_logic = """
            class AvailableVideo(val url: String, val duration: Int, val source: String)
            val combinedAvailableVideos = mutableListOf<AvailableVideo>()

            if (!videoLoaded && pexelsApiKey.isNotBlank()) {
                reportProgress(if (isArabic) "جاري البحث عن مشاهد سينمائية سريعة (Pexels)..." else "Searching for dynamic fast-paced cinematic scenes (Pexels)...", 0.3f)
                try {
                    val pexelsQueries = if (backgroundKeywords.isNotEmpty()) backgroundKeywords.toList() else listOf(
                        "islamic+aesthetics+kaaba+mecca",
                        "dark+cinematic+aesthetic+landscape",
                        "stormy+aesthetic+rainy+window",
                        "moonlight+trees+dark+night",
                        "epic+sunset+clouds+aesthetic",
                        "snowy+mountains+cinematic",
                        "rain+flowers+nature+aesthetic",
                        "sunset+bike+nature+dark"
                    )
                    val chosenQuery = if (!videoQuery.isNullOrBlank()) videoQuery else pexelsQueries.random().replace(" ", "+")
                    val requestUrl = "https://api.pexels.com/videos/search?query=$chosenQuery&orientation=portrait&per_page=30"
                    val request = Request.Builder()
                        .url(requestUrl)
                        .addHeader("Authorization", pexelsApiKey)
                        .build()
                    SystemDiagnosticTracker.addLog("API_CALL", "جاري الاتصال بـ API منصة Pexels للبحث عن مقاطع سينمائية. الكلمة المفتاحية: $chosenQuery")
                    val response = client.newCall(request).execute()
                    if (response.isSuccessful) {
                        val body = response.body?.string() ?: ""
                        val json = JSONObject(body)
                        val videos = json.getJSONArray("videos")
                        SystemDiagnosticTracker.addLog("API_CALL", "استجابة Pexels: نجاح، تم العثور على ${videos.length()} فيديو متاح")
                        for (vIdx in 0 until videos.length()) {
                            val v = videos.getJSONObject(vIdx)
                            val duration = v.optInt("duration", 0)
                            val videoFiles = v.getJSONArray("video_files")
                            val mp4Files = mutableListOf<JSONObject>()
                            for(fIdx in 0 until videoFiles.length()) {
                                val f = videoFiles.getJSONObject(fIdx)
                                if (f.getString("link").contains("mp4", ignoreCase = true)) {
                                    mp4Files.add(f)
                                }
                            }
                            val sortedFiles = mp4Files.sortedByDescending { it.getInt("width") * it.getInt("height") }
                            val highestResUrl = sortedFiles.firstOrNull()?.getString("link")
                            if (highestResUrl != null) {
                                combinedAvailableVideos.add(AvailableVideo(highestResUrl, duration, "Pexels"))
                            }
                        }
                    }
                } catch (e: Exception) {
                    com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
                }
            }

            if (!videoLoaded && pixabayApiKey.isNotBlank()) {
                reportProgress(if (isArabic) "جاري البحث عن مناظر طبيعية هادئة سريعة (Pixabay)..." else "Searching for active nature landscapes (Pixabay)...", 0.3f)
                try {
                    val pixabayQueries = if (backgroundKeywords.isNotEmpty()) backgroundKeywords.toList() else listOf(
                        "islamic+aesthetics",
                        "dark+cinematic+aesthetic+landscape",
                        "stormy+aesthetic+rain",
                        "moonlight+trees+dark+night",
                        "epic+sunset+clouds+aesthetic",
                        "snowy+mountains+cinematic",
                        "rain+nature+aesthetic",
                        "sunset+bike+nature+dark"
                    )
                    val chosenPixabayQuery = if (!videoQuery.isNullOrBlank()) videoQuery else pixabayQueries.random().replace(" ", "+")
                    val request = Request.Builder()
                        .url("https://pixabay.com/api/videos/?key=$pixabayApiKey&q=$chosenPixabayQuery&orientation=vertical&per_page=30")
                        .build()
                    SystemDiagnosticTracker.addLog("API_CALL", "جاري الاتصال بـ API منصة Pixabay للبحث عن مناظر طبيعية. الكلمة المفتاحية: $chosenPixabayQuery")
                    val response = client.newCall(request).execute()
                    if (response.isSuccessful) {
                        val body = response.body?.string() ?: ""
                        val json = JSONObject(body)
                        val hits = json.getJSONArray("hits")
                        SystemDiagnosticTracker.addLog("API_CALL", "استجابة Pixabay: نجاح، تم العثور على ${hits.length()} فيديو متاح")
                        for (hIdx in 0 until hits.length()) {
                            val h = hits.getJSONObject(hIdx)
                            val duration = h.optInt("duration", 0)
                            val videosObj = h.getJSONObject("videos")
                            val sizeKeys = when (videoQuality) {
                                "Normal" -> listOf("small", "tiny", "medium", "large")
                                "High" -> listOf("medium", "small", "large", "tiny")
                                else -> listOf("large", "medium", "small", "tiny")
                            }
                            var selectedVideoUrl: String? = null
                            for (key in sizeKeys) {
                                if (videosObj.has(key)) {
                                    val vObj = videosObj.getJSONObject(key)
                                    val url = vObj.getString("url")
                                    if (url.isNotBlank()) {
                                        selectedVideoUrl = url
                                        break
                                    }
                                }
                            }
                            if (selectedVideoUrl != null) {
                                combinedAvailableVideos.add(AvailableVideo(selectedVideoUrl, duration, "Pixabay"))
                            }
                        }
                    }
                } catch (e: Exception) {
                    com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
                }
            }

            if (!videoLoaded && combinedAvailableVideos.isNotEmpty()) {
                val allChunks = verses.flatMap { it.chunks }
                val numBackgroundVideos = allChunks.size
                
                // Shuffle available videos to ensure variety
                combinedAvailableVideos.shuffle()
                
                for (vidIdx in 0 until numBackgroundVideos) {
                    // Skip fetching if the file already exists (from retry)
                    if (isRetry && chunkIndexToReplace != -1 && vidIdx != chunkIndexToReplace) {
                        continue
                    }
                    val chunk = allChunks[vidIdx]
                    val neededDurSec = ((chunk.endTimeMs - chunk.startTimeMs) / 1000L).toInt() + 2
                    
                    var selectedVideo = combinedAvailableVideos.filter {
                        it.duration >= neededDurSec
                    }.shuffled().firstOrNull()
                    
                    if (selectedVideo == null) {
                        selectedVideo = combinedAvailableVideos.maxByOrNull { it.duration }
                    }
                    
                    if (selectedVideo != null) {
                        if (combinedAvailableVideos.size > 1) {
                            combinedAvailableVideos.remove(selectedVideo)
                        }
                        
                        reportProgress(
                            if (isArabic) "جاري تحميل مشهد متناسق للمقطع ${vidIdx + 1} من ${verses.size}..." else "Downloading duration-matched scene ${vidIdx + 1} of ${verses.size}...",
                            0.35f + (vidIdx * 0.15f / verses.size)
                        )
                        val targetFile = File(context.cacheDir, "bg_video_$vidIdx.mp4")
                        SystemDiagnosticTracker.addLog("DOWNLOAD", "بدء تحميل الخلفية ${vidIdx + 1} من أصل $numBackgroundVideos (${selectedVideo.source})")
                        
                        var success = false
                        try {
                            downloadAudio(selectedVideo.url, targetFile, throwOnError = true)
                            if (targetFile.exists() && targetFile.length() > 0) {
                                success = true
                            }
                        } catch (e: Exception) {
                            SystemDiagnosticTracker.addLog("DOWNLOAD_ERROR", "فشل تحميل الفيديو: ${e.message}")
                        }
                        
                        if (success) {
                            downloadedVideoFiles.add(targetFile)
                            SystemDiagnosticTracker.addLog("DOWNLOAD", "اكتمل تحميل الخلفية ${vidIdx + 1} بنجاح، الحجم: ${targetFile.length()} بايت. متبقي ${numBackgroundVideos - (vidIdx + 1)} خلفيات.")
                        } else {
                            SystemDiagnosticTracker.addLog("DOWNLOAD_ERROR", "فشل تحميل الخلفية ${vidIdx + 1}، ملف الفيديو تالف أو فارغ.")
                        }
                    }
                }
                if (downloadedVideoFiles.isNotEmpty()) {
                    videoLoaded = true
                }
            }
"""

lines = lines[:756] + [new_logic] + lines[967:]

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.writelines(lines)
