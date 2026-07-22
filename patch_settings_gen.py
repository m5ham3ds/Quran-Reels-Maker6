import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

old_logic = '''                                val currentGeminiKey = if (geminiKey.isNotBlank()) geminiKey else com.example.BuildConfig.GEMINI_API_KEY
                                if (currentGeminiKey.isBlank() || currentGeminiKey == "MY_GEMINI_API_KEY") return@Button
                                isGenerating = true
                                showInlineDiagnostics = true
                                com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "بدء عملية الملئ التلقائي للكلمات المرجعية...")
                                scope.launch(Dispatchers.IO) {
                                    try {
                                        val client = OkHttpClient.Builder()
                                            // Bypass WAF error
                                            .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .writeTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .addInterceptor { chain ->
                                                val original = chain.request()
                                                val requestBuilder = original.newBuilder()
                                                    .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                                                    .header("x-goog-api-key", currentGeminiKey.trim())
                                                    .method(original.method, original.body)
                                                chain.proceed(requestBuilder.build())
                                            }
                                            .build()
                                        val modelToUse = geminiModel.trim()
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
                                            .build()
                                        var attempt = 0
                                        var success = false
                                        while (attempt < 3 && !success) {
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "بدء المحاولة رقم ${attempt + 1}")
                                            val response = client.newCall(request).execute()
                                            if (response.isSuccessful) {
                                                val body = response.body?.string() ?: ""
                                                val root = JSONObject(body)
                                                val textStr = root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")
                                                val newSet = backgroundKeywords.toMutableSet()
                                                textStr.split(",").forEach {
                                                    val trimmed = it.trim().removeSurrounding("\"").removeSurrounding("'").removeSurrounding("\n")
                                                    if (trimmed.isNotBlank()) newSet.add(trimmed)
                                                }'''

new_logic = '''                                val apiKey = if (aiPlatform == "HuggingFace") huggingfaceKey else if (geminiKey.isNotBlank()) geminiKey else com.example.BuildConfig.GEMINI_API_KEY
                                if (apiKey.isBlank() || apiKey == "MY_GEMINI_API_KEY") {
                                    com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "يرجى إدخال مفتاح API أولاً.")
                                    return@Button
                                }
                                isGenerating = true
                                showInlineDiagnostics = true
                                com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "بدء عملية الملئ التلقائي للكلمات المرجعية...")
                                scope.launch(Dispatchers.IO) {
                                    try {
                                        val client = OkHttpClient.Builder()
                                            // Bypass WAF error
                                            .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .writeTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                                            .addInterceptor { chain ->
                                                val original = chain.request()
                                                val requestBuilder = original.newBuilder()
                                                    .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                                                
                                                if (aiPlatform == "Gemini") {
                                                    requestBuilder.header("x-goog-api-key", apiKey.trim())
                                                }
                                                
                                                requestBuilder.method(original.method, original.body)
                                                chain.proceed(requestBuilder.build())
                                            }
                                            .build()
                                            
                                        val request: Request
                                        if (aiPlatform == "HuggingFace") {
                                            val modelToUse = huggingfaceModel.trim()
                                            val url = "https://api-inference.huggingface.co/models/${modelToUse}/v1/chat/completions"
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "الرابط المطلوب: $url")
                                            val jsonReq = JSONObject().apply {
                                                put("model", modelToUse)
                                                put("messages", org.json.JSONArray().apply {
                                                    put(JSONObject().apply {
                                                        put("role", "system")
                                                        put("content", "You are a helpful assistant.")
                                                    })
                                                    put(JSONObject().apply {
                                                        put("role", "user")
                                                        put("content", "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings. Do not include any explanations.")
                                                    })
                                                })
                                                put("temperature", 0.7)
                                                put("max_tokens", 200)
                                            }
                                            request = Request.Builder()
                                                .url(url)
                                                .header("Authorization", "Bearer ${apiKey.trim()}")
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        } else {
                                            val modelToUse = geminiModel.trim()
                                            val url = "https://generativelanguage.googleapis.com/v1beta/models/${modelToUse}:generateContent?key=${apiKey.trim()}"
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
                                            request = Request.Builder()
                                                .url(url)
                                                .post(jsonReq.toString().toRequestBody("application/json".toMediaTypeOrNull()))
                                                .build()
                                        }
                                        
                                        var attempt = 0
                                        var success = false
                                        while (attempt < 3 && !success) {
                                            com.example.generator.SystemDiagnosticTracker.addLog("AUTOFILL", "بدء المحاولة رقم ${attempt + 1}")
                                            val response = client.newCall(request).execute()
                                            if (response.isSuccessful) {
                                                val body = response.body?.string() ?: ""
                                                val root = JSONObject(body)
                                                
                                                var textStr = ""
                                                if (aiPlatform == "HuggingFace") {
                                                    val choices = root.optJSONArray("choices")
                                                    if (choices != null && choices.length() > 0) {
                                                        val message = choices.getJSONObject(0).optJSONObject("message")
                                                        textStr = message?.optString("content", "")?.trim() ?: ""
                                                    }
                                                } else {
                                                    textStr = root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")
                                                }
                                                
                                                val newSet = backgroundKeywords.toMutableSet()
                                                textStr.split(",").forEach {
                                                    val trimmed = it.trim().removeSurrounding("\"").removeSurrounding("'").removeSurrounding("\\n")
                                                    if (trimmed.isNotBlank()) newSet.add(trimmed)
                                                }'''

content = content.replace(old_logic, new_logic)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
