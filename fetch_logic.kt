                            downloadedVideoFiles.addAll(bgFiles)
                            videoLoaded = true
                        }
                    }
                } catch (ex: Exception) {}
            }
            
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
                        if (videos.length() > 0) {
                            val availableVideosList = mutableListOf<JSONObject>()
                            for (vIdx in 0 until videos.length()) {
                                availableVideosList.add(videos.getJSONObject(vIdx))
                            }
                            
                            val allChunks = verses.flatMap { it.chunks }
                            val numBackgroundVideos = allChunks.size
                            for (vidIdx in 0 until numBackgroundVideos) {
                                // Skip fetching if the file already exists (from retry)
                                if (isRetry && chunkIndexToReplace != -1 && vidIdx != chunkIndexToReplace) {
                                    continue
                                }
                                val chunk = allChunks[vidIdx]
                                val neededDurSec = ((chunk.endTimeMs - chunk.startTimeMs) / 1000L).toInt() + 2
                                
                                // Try to find a video with duration >= neededDurSec, otherwise find the longest video
                                var selectedVideoJson = availableVideosList.filter {
                                    it.optInt("duration", 0) >= neededDurSec
                                }.shuffled().firstOrNull()
                                
                                if (selectedVideoJson == null) {
                                    selectedVideoJson = availableVideosList.maxByOrNull { it.optInt("duration", 0) }
                                }
                                
                                if (selectedVideoJson != null) {
                                    // Remove selected video from lists to maintain variety
                                    if (availableVideosList.size > 1) {
                                        availableVideosList.remove(selectedVideoJson)
                                    }
                                    
                                    val videoFiles = selectedVideoJson.getJSONArray("video_files")
                                    var highestResUrl: String? = null
                                    
                                    val mp4Files = mutableListOf<JSONObject>()
                                    for(v in 0 until videoFiles.length()) {
                                        val f = videoFiles.getJSONObject(v)
                                        if (f.getString("link").contains("mp4", ignoreCase = true)) {
                                            mp4Files.add(f)
                                        }
                                    }
                                    
                                    val portraitFiles = mp4Files.filter { it.optInt("width", 0) < it.optInt("height", 0) }
                                    val targetList = if(portraitFiles.isNotEmpty()) portraitFiles else mp4Files
                                    
                                    if (targetList.isNotEmpty()) {
                                        val sortedFiles = targetList.sortedBy { it.optInt("width", 0) * it.optInt("height", 0) }
                                        highestResUrl = when(videoQuality) {
                                            "Normal" -> {
                                                // Try to pick a medium-low one, bounded so it's not absolutely terrible.
                                                val idx = (sortedFiles.size * 0.25).toInt()
                                                sortedFiles[idx.coerceAtMost(sortedFiles.lastIndex)].getString("link")
                                            }
                                            "High" -> {
                                                // Try to pick a medium-high one.
                                                val idx = (sortedFiles.size * 0.6).toInt()
                                                sortedFiles[idx.coerceAtMost(sortedFiles.lastIndex)].getString("link")
                                            }
                                            else -> {
                                                // "Ultra" - Maximum resolution
                                                sortedFiles.last().getString("link")
                                            }
                                        }
                                    } else if (videoFiles.length() > 0) {
                                        highestResUrl = videoFiles.getJSONObject(0).getString("link")
                                    }
                                    
                                    var selectedVideoUrl: String? = highestResUrl
                                    
                                    if (selectedVideoUrl != null) {
                                        reportProgress(
                                            if (isArabic) "جاري تحميل مشهد متناسق للمقطع ${vidIdx + 1} من ${verses.size}..." else "Downloading duration-matched scene ${vidIdx + 1} of ${verses.size}...",
                                            0.35f + (vidIdx * 0.15f / verses.size)
                                        )
                                        val targetFile = File(context.cacheDir, "bg_video_$vidIdx.mp4")
                                        SystemDiagnosticTracker.addLog("DOWNLOAD", "بدء تحميل الخلفية ${vidIdx + 1} من أصل $numBackgroundVideos (Pexels)")
                                        runCatching { downloadAudio(selectedVideoUrl, targetFile, throwOnError = false) }.onFailure { e -> SystemDiagnosticTracker.addLog("DOWNLOAD_ERROR", "فشل تحميل الفيديو: ${e.message}") }
                                        downloadedVideoFiles.add(targetFile)
                                        SystemDiagnosticTracker.addLog("DOWNLOAD", "اكتمل تحميل الخلفية ${vidIdx + 1} بنجاح، الحجم: ${targetFile.length()} بايت. متبقي ${numBackgroundVideos - (vidIdx + 1)} خلفيات.")
                                    }
                                }
                            }
                            if (downloadedVideoFiles.isNotEmpty()) {
                                videoLoaded = true
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
                        if (hits.length() > 0) {
                            val availableHitsList = mutableListOf<JSONObject>()
                            for (hIdx in 0 until hits.length()) {
                                availableHitsList.add(hits.getJSONObject(hIdx))
                            }
                            
                            val allChunks = verses.flatMap { it.chunks }
                            val numBackgroundVideos = allChunks.size
                            for (vidIdx in 0 until numBackgroundVideos) {
                                // Skip fetching if the file already exists (from retry)
                                if (isRetry && chunkIndexToReplace != -1 && vidIdx != chunkIndexToReplace) {
                                    continue
                                }
                                val chunk = allChunks[vidIdx]
                                val neededDurSec = ((chunk.endTimeMs - chunk.startTimeMs) / 1000L).toInt() + 2
                                
                                var selectedHit = availableHitsList.filter {
                                    it.optInt("duration", 0) >= neededDurSec
                                }.shuffled().firstOrNull()
                                
                                if (selectedHit == null) {
                                    selectedHit = availableHitsList.maxByOrNull { it.optInt("duration", 0) }
                                }
                                
                                if (selectedHit != null) {
                                    if (availableHitsList.size > 1) {
                                        availableHitsList.remove(selectedHit)
                                    }
                                    
                                    val videosObj = selectedHit.getJSONObject("videos")
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
                                        reportProgress(
                                            if (isArabic) "جاري تحميل مشهد متناسق للمقطع ${vidIdx + 1} من ${verses.size}..." else "Downloading duration-matched scene ${vidIdx + 1} of ${verses.size}...",
                                            0.35f + (vidIdx * 0.15f / verses.size)
                                        )
                                        val targetFile = File(context.cacheDir, "bg_video_$vidIdx.mp4")
                                        SystemDiagnosticTracker.addLog("DOWNLOAD", "بدء تحميل الخلفية ${vidIdx + 1} من أصل $numBackgroundVideos (Pixabay)")
                                        runCatching { downloadAudio(selectedVideoUrl, targetFile, throwOnError = false) }.onFailure { e -> SystemDiagnosticTracker.addLog("DOWNLOAD_ERROR", "فشل تحميل الفيديو: ${e.message}") }
                                        downloadedVideoFiles.add(targetFile)
                                        SystemDiagnosticTracker.addLog("DOWNLOAD", "اكتمل تحميل الخلفية ${vidIdx + 1} بنجاح، الحجم: ${targetFile.length()} بايت. متبقي ${numBackgroundVideos - (vidIdx + 1)} خلفيات.")
                                    }
                                }
                            }
                            if (downloadedVideoFiles.isNotEmpty()) {
                                videoLoaded = true
                            }
                        }
                    }
                } catch (e: Exception) {
                    com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
                }
            }
            
            // Fallback to high-quality direct public video CDN loop URLs so we NEVER show a blank background or static image
            if (!videoLoaded) {
                checkCancellationAndPause()
                reportProgress(if (isArabic) "جاري تحميل مشاهد طبيعية متحركة عالية الجودة..." else "Downloading premium cinematic video loops...", 0.3f)
                val directUrls = listOf(
                    "https://assets.mixkit.co/videos/preview/mixkit-vertical-shot-of-a-beautiful-waterfall-in-a-forest-43756-large.mp4"
                )
                val countToLoad = 1
                SystemDiagnosticTracker.addLog("DOWNLOAD", "بدء تحميل خلفيات الطوارئ المباشرة. العدد المطلوب: $countToLoad")
                for (vidIdx in 0 until countToLoad) {
                    if (isRetry && chunkIndexToReplace != -1 && vidIdx != chunkIndexToReplace) continue
                    try {
                        reportProgress(
                            if (isArabic) "جاري تحميل مشهد سينمائي عالي الجودة ${vidIdx + 1} من $countToLoad..." else "Loading cinematic nature loop ${vidIdx + 1} of $countToLoad...",
                            0.35f + (vidIdx * 0.15f / countToLoad)
                        )
                        val targetFile = File(context.cacheDir, "bg_video_$vidIdx.mp4")
                        SystemDiagnosticTracker.addLog("DOWNLOAD", "بدء تحميل خلفية الطوارئ ${vidIdx + 1} من أصل $countToLoad")
                        try {
                            downloadAudio(directUrls[vidIdx], targetFile, throwOnError = false)
                        } catch (e: Exception) {
                            SystemDiagnosticTracker.addLog("DOWNLOAD_ERROR", "فشل تحميل فيديو الطوارئ: ${e.message}")
                        }
                        if (targetFile.exists() && targetFile.length() > 0) {
                            downloadedVideoFiles.add(targetFile)
                            SystemDiagnosticTracker.addLog("DOWNLOAD", "اكتمل تحميل خلفية الطوارئ ${vidIdx + 1} بنجاح، الحجم: ${targetFile.length()} بايت. متبقي ${countToLoad - (vidIdx + 1)} خلفيات.")
                        }
                    } catch (e: Exception) {
                        com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
                    }
                }
                if (downloadedVideoFiles.isNotEmpty()) {
                    videoLoaded = true
                }
            }
            
            downloadedVideoFiles.sortBy {
                val numMatch = Regex("\\d+").find(it.name)
