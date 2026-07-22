import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

start_marker = 'val url = "https://generativelanguage.googleapis.com/v1beta/models/${modelToUse}:generateContent?key=${currentGeminiKey.trim()}"'
end_marker = 'val request = Request.Builder()'

replacement = """
                                        val request: Request
                                        if (aiPlatform == "HuggingFace") {
                                            val hfKey = huggingfaceKey.trim()
                                            if (hfKey.isBlank()) throw Exception("HuggingFace API key is missing")
                                            val hfModel = huggingfaceModel.ifBlank { "Qwen/Qwen2.5-72B-Instruct" }.trim()
                                            val hfUrl = "https://api-inference.huggingface.co/models/$hfModel/v1/chat/completions"
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب: $hfUrl")
                                            val jsonReq = JSONObject().apply {
                                                put("model", hfModel)
                                                put("messages", org.json.JSONArray().apply {
                                                    put(JSONObject().apply {
                                                        put("role", "system")
                                                        put("content", "You must reply ONLY with a comma-separated list of strings.")
                                                    })
                                                    put(JSONObject().apply {
                                                        put("role", "user")
                                                        put("content", backgroundKeywordsPrompt.ifBlank { "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings." })
                                                    })
                                                })
                                            }
                                            request = Request.Builder()
                                                .url(hfUrl)
                                                .header("Authorization", "Bearer $hfKey")
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        } else {
                                            val modelToUse = geminiModel.trim()
                                            val url = "https://generativelanguage.googleapis.com/v1beta/models/${modelToUse}:generateContent?key=${currentGeminiKey.trim()}"
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب: $url")
                                            val jsonReq = JSONObject().apply {
                                                put("contents", org.json.JSONArray().apply {
                                                    put(JSONObject().apply {
                                                        put("parts", org.json.JSONArray().apply {
                                                            put(JSONObject().apply {
                                                                put("text", backgroundKeywordsPrompt.ifBlank { "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings." })
                                                            })
                                                        })
                                                    })
                                                })
                                            }
                                            request = Request.Builder()
                                                .url(url)
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        }
"""

if start_marker in content and end_marker in content:
    idx1 = content.find(start_marker)
    # find the line before start_marker
    prefix = content[:idx1]
    
    # find val modelToUse
    model_idx = prefix.rfind('val modelToUse')
    if model_idx != -1:
        idx1 = model_idx
        
    idx2 = content.find('.build()', content.find(end_marker)) + 8
    
    content = content[:idx1] + replacement + content[idx2:]
    
    with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Markers not found!")
