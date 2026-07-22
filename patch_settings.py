import re

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'r') as f:
    content = f.read()

# Add keys
content = content.replace(
    'val GEMINI_PROMPT = stringPreferencesKey("gemini_prompt")',
    '''val GEMINI_PROMPT = stringPreferencesKey("gemini_prompt")
        val AI_PLATFORM = stringPreferencesKey("ai_platform")
        val HUGGINGFACE_API_KEY = stringPreferencesKey("huggingface_api_key")
        val HUGGINGFACE_MODEL = stringPreferencesKey("huggingface_model")'''
)

# Add flows
content = content.replace(
    'val geminiPrompt: Flow<String> = context.dataStore.data.map { it[GEMINI_PROMPT] ?: """',
    '''val aiPlatform: Flow<String> = context.dataStore.data.map { it[AI_PLATFORM] ?: "Gemini" }
    val huggingfaceApiKey: Flow<String> = context.dataStore.data.map { it[HUGGINGFACE_API_KEY] ?: "" }
    val huggingfaceModel: Flow<String> = context.dataStore.data.map { it[HUGGINGFACE_MODEL] ?: "Qwen/Qwen2.5-72B-Instruct" }
    
    val geminiPrompt: Flow<String> = context.dataStore.data.map { it[GEMINI_PROMPT] ?: """'''
)

# Add save functions
content = content.replace(
    'suspend fun saveGeminiKey(key: String) {',
    '''suspend fun saveAiPlatform(platform: String) {
        context.dataStore.edit { it[AI_PLATFORM] = platform }
    }
    
    suspend fun saveHuggingfaceApiKey(key: String) {
        context.dataStore.edit { it[HUGGINGFACE_API_KEY] = key }
    }
    
    suspend fun saveHuggingfaceModel(model: String) {
        context.dataStore.edit { it[HUGGINGFACE_MODEL] = model }
    }

    suspend fun saveGeminiKey(key: String) {'''
)

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'w') as f:
    f.write(content)
