import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'val prompt = SystemPromptTemplate.getAlignmentPrompt(arabicChunks, fullTranslation)' in line:
        start_idx = i
    if 'return@withContext null' in line and i > 3000:
        end_idx = i - 1

if start_idx != -1 and end_idx != -1:
    new_gen = '''        val prompt = SystemPromptTemplate.getAlignmentPrompt(arabicChunks, fullTranslation)
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
        }\n'''
    lines = lines[:start_idx] + [new_gen] + lines[end_idx:]

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.writelines(lines)
