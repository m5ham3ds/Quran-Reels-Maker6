import re

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val GEMINI_PROMPT = stringPreferencesKey("gemini_prompt")',
    'val GEMINI_PROMPT = stringPreferencesKey("gemini_prompt")\n        val BACKGROUND_KEYWORDS_PROMPT = stringPreferencesKey("background_keywords_prompt")'
)

if 'val backgroundKeywordsPrompt' not in content:
    content = content.replace(
        'val geminiPrompt: Flow<String> =',
        '''val backgroundKeywordsPrompt: Flow<String> = context.dataStore.data.map { it[BACKGROUND_KEYWORDS_PROMPT] ?: "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings." }
    
    val geminiPrompt: Flow<String> ='''
    )

if 'suspend fun saveGeminiPrompt' not in content:
    pass
else:
    content = content.replace(
        'suspend fun saveGeminiPrompt(prompt: String) {',
        '''suspend fun saveBackgroundKeywordsPrompt(prompt: String) {
        context.dataStore.edit { it[BACKGROUND_KEYWORDS_PROMPT] = prompt }
    }

    suspend fun saveGeminiPrompt(prompt: String) {'''
    )

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'w') as f:
    f.write(content)
