import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

old_ai_init = '''        val settingsManager = SettingsManager(context)
        var apiKey = settingsManager.geminiApiKey.first()
        val geminiModel = settingsManager.geminiModel.first().ifBlank { "gemini-1.5-pro" }
        if (apiKey.isBlank()) {
            apiKey = com.example.BuildConfig.GEMINI_API_KEY
        }'''

new_ai_init = '''        val settingsManager = SettingsManager(context)
        val aiPlatform = settingsManager.aiPlatform.first()
        var apiKey = if (aiPlatform == "HuggingFace") settingsManager.huggingfaceApiKey.first() else settingsManager.geminiApiKey.first()
        val model = if (aiPlatform == "HuggingFace") settingsManager.huggingfaceModel.first().ifBlank { "Qwen/Qwen2.5-72B-Instruct" } else settingsManager.geminiModel.first().ifBlank { "gemini-1.5-pro" }
        if (apiKey.isBlank() && aiPlatform == "Gemini") {
            apiKey = com.example.BuildConfig.GEMINI_API_KEY
        }'''
content = content.replace(old_ai_init, new_ai_init)


old_ai_req = '''        val prompt = SystemPromptTemplate.getAlignmentPrompt(arabicChunks, fullTranslation)
        val jsonRequest = JSONObject().apply {
            val partsArray = org.json.JSONArray().apply {
                put(JSONObject().apply {
                    put("text", prompt)
                })
            }
            val countArray = org.json.JSONArray().apply {
                put(JSONObject().apply {
                    put("parts", partsArray)
                })
            }
            put("contents", countArray)
            put("generationConfig", JSONObject().apply {
                put("responseMimeType", "application/json")
                put("temperature", 0.1)
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
            var attempt = 0
            val maxAttempts = 3
            while (attempt < maxAttempts) {
                val response = client.newCall(request).execute()
                if (response.isSuccessful) {
                    val responseStr = response.body?.string() ?: ""
                    val rootJson = JSONObject(responseStr)
                    val candidates = rootJson.getJSONArray("candidates")
                    if (candidates.length() > 0) {
                        val candidate = candidates.getJSONObject(0)
                        val contentObj = candidate.getJSONObject("content")
                        val parts = contentObj.getJSONArray("parts")
                        if (parts.length() > 0) {
                            val rawText = parts.getJSONObject(0).getString("text").trim()
                            val cleanText = if (rawText.startsWith("```json")) {
                                rawText.substringAfter("```json").substringBeforeLast("```").trim()
                            } else if (rawText.startsWith("```")) {
                                rawText.substringAfter("```").substringBeforeLast("```").trim()
                            } else {
                                rawText
                            }
                            val jsonOutput = JSONObject(cleanText)
                            if (jsonOutput.has("aligned_translations")) {
                                val arr = jsonOutput.getJSONArray("aligned_translations")
                                val chunksList = mutableListOf<String>()
                                for (i in 0 until arr.length()) {
                                    chunksList.add(arr.getString(i))
                                }
                                if (chunksList.size == arabicChunks.size) {
                                    return@withContext chunksList
                                }
                            }
                        }
                    }
                    break
                } else if (response.code == 429) {
                    if (attempt < maxAttempts - 1) {
                        attempt++
                        kotlinx.coroutines.delay(2000L * attempt)
                        continue
                    } else {
                        break
                    }
                } else {
                    break
                }
            }
        } catch (e: Exception) {
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
        }'''

new_ai_req = '''        val prompt = SystemPromptTemplate.getAlignmentPrompt(arabicChunks, fullTranslation)
        val request: Request
        if (aiPlatform == "HuggingFace") {
            val jsonRequest = JSONObject().apply {
                put("model", model.trim())
                put("messages", org.json.JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "system")
                        put("content", "You must reply ONLY in JSON format. Do not use Markdown formatting.")
                    })
                    put(JSONObject().apply {
                        put("role", "user")
                        put("content", prompt)
                    })
                })
                put("temperature", 0.1)
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
                val partsArray = org.json.JSONArray().apply {
                    put(JSONObject().apply {
                        put("text", prompt)
                    })
                }
                val countArray = org.json.JSONArray().apply {
                    put(JSONObject().apply {
                        put("parts", partsArray)
                    })
                }
                put("contents", countArray)
                put("generationConfig", JSONObject().apply {
                    put("responseMimeType", "application/json")
                    put("temperature", 0.1)
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
            var attempt = 0
            val maxAttempts = 3
            while (attempt < maxAttempts) {
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
                    
                    val cleanText = if (rawText.startsWith("```json")) {
                        rawText.substringAfter("```json").substringBeforeLast("```").trim()
                    } else if (rawText.startsWith("```")) {
                        rawText.substringAfter("```").substringBeforeLast("```").trim()
                    } else {
                        rawText
                    }
                    
                    try {
                        val jsonOutput = JSONObject(cleanText)
                        if (jsonOutput.has("aligned_translations")) {
                            val arr = jsonOutput.getJSONArray("aligned_translations")
                            val chunksList = mutableListOf<String>()
                            for (i in 0 until arr.length()) {
                                chunksList.add(arr.getString(i))
                            }
                            if (chunksList.size == arabicChunks.size) {
                                return@withContext chunksList
                            }
                        }
                    } catch(e: Exception) {
                        SystemDiagnosticTracker.addLog("AI", "JSON parsing error: ${e.message}")
                    }
                    break
                } else if (response.code == 429 || response.code >= 500) {
                    if (attempt < maxAttempts - 1) {
                        attempt++
                        kotlinx.coroutines.delay(2000L * attempt)
                        continue
                    } else {
                        break
                    }
                } else {
                    break
                }
            }
        } catch (e: Exception) {
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
        }'''
content = content.replace(old_ai_req, new_ai_req)

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)
