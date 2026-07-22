import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

target = '''                                        val modelToUse = geminiModel.trim()
                                        val url = "https://generativelanguage.googleapis.com/v1beta/models/${modelToUse}:generateContent?key=${currentGeminiKey.trim()}"
                                        com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب: $url")
                                        val jsonReq = JSONObject().apply {
                                            put("contents", org.json.JSONArray().apply {
                                                put(JSONObject().apply {
                                                    put("parts", org.json.JSONArray().apply {
                                                        put(JSONObject().apply {
                                                            put("text", "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings.")
                                                        })
                                                    })
                                                })
                                            })
                                        }
                                        val request = Request.Builder()
                                            .url(url)
                                            .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                            .build()'''

replacement = '''                                        val isHuggingFace = aiPlatform == "HuggingFace"
                                        val promptText = backgroundKeywordsPrompt.ifBlank { "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings." }
                                        
                                        val request = if (isHuggingFace) {
                                            val url = "https://api-inference.huggingface.co/models/${huggingfaceModel.trim()}/v1/chat/completions"
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب (HuggingFace): $url")
                                            val jsonReq = JSONObject().apply {
                                                put("model", huggingfaceModel.trim())
                                                put("messages", org.json.JSONArray().apply {
                                                    put(JSONObject().apply {
                                                        put("role", "user")
                                                        put("content", promptText)
                                                    })
                                                })
                                                put("max_tokens", 100)
                                            }
                                            Request.Builder()
                                                .url(url)
                                                .header("Authorization", "Bearer ${huggingfaceKey.trim()}")
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        } else {
                                            val modelToUse = geminiModel.trim()
                                            val url = "https://generativelanguage.googleapis.com/v1beta/models/${modelToUse}:generateContent?key=${currentGeminiKey.trim()}"
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب (Gemini): $url")
                                            val jsonReq = JSONObject().apply {
                                                put("contents", org.json.JSONArray().apply {
                                                    put(JSONObject().apply {
                                                        put("parts", org.json.JSONArray().apply {
                                                            put(JSONObject().apply {
                                                                put("text", promptText)
                                                            })
                                                        })
                                                    })
                                                })
                                            }
                                            Request.Builder()
                                                .url(url)
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        }'''
content = content.replace(target, replacement)

target2 = '''                                                val textStr = root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")'''

replacement2 = '''                                                val textStr = if (isHuggingFace) {
                                                    root.getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
                                                } else {
                                                    root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")
                                                }'''

content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
