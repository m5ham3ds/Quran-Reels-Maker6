import re

with open('app/src/main/java/com/example/generator/GeminiMetaGenerator.kt', 'r') as f:
    content = f.read()

# Replace initialization
old_init = '''        val settingsManager = SettingsManager(context)
        val apiKey = settingsManager.geminiApiKey.first()
        var geminiModel = settingsManager.geminiModel.first().ifBlank { "gemini-1.5-pro" }
        
        if (apiKey.isBlank()) {
            return@withContext ClipAnalysisResult(0f, "", "Gemini API key is missing")
        }'''

new_init = '''        val settingsManager = SettingsManager(context)
        val aiPlatform = settingsManager.aiPlatform.first()
        val apiKey = if (aiPlatform == "HuggingFace") settingsManager.huggingfaceApiKey.first() else settingsManager.geminiApiKey.first()
        val model = if (aiPlatform == "HuggingFace") settingsManager.huggingfaceModel.first().ifBlank { "Qwen/Qwen2.5-72B-Instruct" } else settingsManager.geminiModel.first().ifBlank { "gemini-1.5-pro" }
        
        if (apiKey.isBlank()) {
            return@withContext ClipAnalysisResult(0f, "", "${if (aiPlatform == "HuggingFace") "HuggingFace" else "Gemini"} API key is missing")
        }'''
content = content.replace(old_init, new_init)

# Replace the generation logic
old_gen = '''        val jsonRequest = JSONObject().apply {
            put("contents", JSONArray().apply {
                put(JSONObject().apply {
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply {
                            put("text", prompt)
                        })
                    })
                })
            })
            put("generationConfig", JSONObject().apply {
                put("response_mime_type", "application/json")
                put("temperature", 0.2)
            })
        }
        val requestBody = jsonRequest.toString().toRequestBody("application/json".toMediaTypeOrNull())
        val url = "https://generativelanguage.googleapis.com/v1beta/models/${geminiModel.trim()}:generateContent?key=${apiKey.trim()}"
        val request = Request.Builder()
            .url(url)
            .header("x-goog-api-key", apiKey.trim())
            .post(requestBody)
            .build()
        
        try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                val responseStr = response.body?.string() ?: ""
                val rootJson = JSONObject(responseStr)
                val candidates = rootJson.optJSONArray("candidates")
                if (candidates != null && candidates.length() > 0) {
                    val candidate = candidates.getJSONObject(0)
                    val contentObj = candidate.getJSONObject("content")
                    val parts = contentObj.getJSONArray("parts")
                    if (parts.length() > 0) {
                        var rawText = parts.getJSONObject(0).getString("text").trim()
                        SystemDiagnosticTracker.addLog("GEMINI", "Raw Gemini Response: $rawText")
                        
                        if (rawText.startsWith("```json")) {
                            rawText = rawText.substringAfter("```json").substringBeforeLast("```").trim()
                        } else if (rawText.startsWith("```")) {
                            rawText = rawText.substringAfter("```").substringBeforeLast("```").trim()
                        }
                        
                        try {
                            val jsonOutput = JSONObject(rawText)
                            return@withContext ClipAnalysisResult(
                                relevance = 1.0f,
                                analysis = "OK",
                                surah = jsonOutput.optInt("surah", 1),
                                startAyah = jsonOutput.optInt("startAyah", 1),
                                endAyah = jsonOutput.optInt("endAyah", 5),
                                reciterName = jsonOutput.optString("reciterName", "غير معروف"),
                                title = jsonOutput.optString("title", "تلاوة خاشعة"),
                                category = jsonOutput.optString("category", "سكينة")
                            )
                        } catch (e: Exception) {
                            SystemDiagnosticTracker.addLog("GEMINI", "❌ خطأ في تحليل استجابة Gemini: ${e.message}")
                            return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "فشل تحليل معلومات المقطع من الذكاء الاصطناعي")
                        }
                    }
                }
            } else {
                val errorBody = response.body?.string() ?: ""
                SystemDiagnosticTracker.addLog("GEMINI", "HTTP Error ${response.code}: $errorBody")
                return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "حدث خطأ في الاستجابة: ${response.code} - ${if (response.code == 503) "النموذج يواجه ضغطاً كبيراً، يرجى المحاولة لاحقاً أو تغيير النموذج" else "غير معروف"}")
            }
        } catch (e: Exception) {
            SystemDiagnosticTracker.addLog("GEMINI", "Error calling Gemini: ${e.message}")
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
            return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "خطأ في الاتصال بالذكاء الاصطناعي: ${e.message}")
        }'''

new_gen = '''        val request: Request
        if (aiPlatform == "HuggingFace") {
            val jsonRequest = JSONObject().apply {
                put("model", model.trim())
                put("messages", JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "system")
                        put("content", "You must reply ONLY in JSON format, without any markdown formatting or explanations.")
                    })
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", prompt)
                    })
                })
                put("temperature", 0.2)
                put("max_tokens", 1000)
            }
            val requestBody = jsonRequest.toString().toRequestBody("application/json".toMediaTypeOrNull())
            val url = "https://api-inference.huggingface.co/models/${model.trim()}/v1/chat/completions"
            request = Request.Builder()
                .url(url)
                .header("Authorization", "Bearer ${apiKey.trim()}")
                .post(requestBody)
                .build()
        } else {
            val jsonRequest = JSONObject().apply {
                put("contents", JSONArray().apply {
                    put(JSONObject().apply {
                        put("parts", JSONArray().apply {
                            put(JSONObject().apply {
                                put("text", prompt)
                            })
                        })
                    })
                })
                put("generationConfig", JSONObject().apply {
                    put("response_mime_type", "application/json")
                    put("temperature", 0.2)
                })
            }
            val requestBody = jsonRequest.toString().toRequestBody("application/json".toMediaTypeOrNull())
            val url = "https://generativelanguage.googleapis.com/v1beta/models/${model.trim()}:generateContent?key=${apiKey.trim()}"
            request = Request.Builder()
                .url(url)
                .header("x-goog-api-key", apiKey.trim())
                .post(requestBody)
                .build()
        }
        
        try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                val responseStr = response.body?.string() ?: ""
                val rootJson = JSONObject(responseStr)
                
                var rawText = ""
                if (aiPlatform == "HuggingFace") {
                    val choices = rootJson.optJSONArray("choices")
                    if (choices != null && choices.length() > 0) {
                        val message = choices.getJSONObject(0).optJSONObject("message")
                        rawText = message?.optString("content", "")?.trim() ?: ""
                    }
                } else {
                    val candidates = rootJson.optJSONArray("candidates")
                    if (candidates != null && candidates.length() > 0) {
                        val candidate = candidates.getJSONObject(0)
                        val contentObj = candidate.getJSONObject("content")
                        val parts = contentObj.getJSONArray("parts")
                        if (parts.length() > 0) {
                            rawText = parts.getJSONObject(0).getString("text").trim()
                        }
                    }
                }
                
                SystemDiagnosticTracker.addLog("AI", "Raw AI Response: $rawText")
                
                if (rawText.startsWith("```json")) {
                    rawText = rawText.substringAfter("```json").substringBeforeLast("```").trim()
                } else if (rawText.startsWith("```")) {
                    rawText = rawText.substringAfter("```").substringBeforeLast("```").trim()
                }
                
                try {
                    val jsonOutput = JSONObject(rawText)
                    return@withContext ClipAnalysisResult(
                        relevance = 1.0f,
                        analysis = "OK",
                        surah = jsonOutput.optInt("surah", 1),
                        startAyah = jsonOutput.optInt("startAyah", 1),
                        endAyah = jsonOutput.optInt("endAyah", 5),
                        reciterName = jsonOutput.optString("reciterName", "غير معروف"),
                        title = jsonOutput.optString("title", "تلاوة خاشعة"),
                        category = jsonOutput.optString("category", "سكينة")
                    )
                } catch (e: Exception) {
                    SystemDiagnosticTracker.addLog("AI", "❌ خطأ في تحليل استجابة الذكاء الاصطناعي: ${e.message}")
                    return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "فشل تحليل معلومات المقطع من الذكاء الاصطناعي")
                }
            } else {
                val errorBody = response.body?.string() ?: ""
                SystemDiagnosticTracker.addLog("AI", "HTTP Error ${response.code}: $errorBody")
                return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "حدث خطأ في الاستجابة: ${response.code} - ${if (response.code == 503) "النموذج يواجه ضغطاً كبيراً، يرجى المحاولة لاحقاً أو تغيير النموذج" else "غير معروف"}")
            }
        } catch (e: Exception) {
            SystemDiagnosticTracker.addLog("AI", "Error calling AI: ${e.message}")
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
            return@withContext ClipAnalysisResult(relevance = 0f, analysis = "", error = "خطأ في الاتصال بالذكاء الاصطناعي: ${e.message}")
        }'''
content = content.replace(old_gen, new_gen)

with open('app/src/main/java/com/example/generator/GeminiMetaGenerator.kt', 'w') as f:
    f.write(content)
