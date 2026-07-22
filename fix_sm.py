import re

with open("app/src/main/java/com/example/settings/SettingsManager.kt", "r") as f:
    sm = f.read()

sm = sm.replace("val TEXT_ANIMATION = stringPreferencesKey(\"text_animation\")", "val TEXT_ANIMATION = stringPreferencesKey(\"text_animation\")\n        val TEXT_ANIMATION_ENABLED = booleanPreferencesKey(\"text_animation_enabled\")")

sm = sm.replace("val textAnimation: Flow<String> = context.dataStore.data.map { it[TEXT_ANIMATION] ?: \"Scale\" }", "val textAnimation: Flow<String> = context.dataStore.data.map { it[TEXT_ANIMATION] ?: \"Scale\" }\n    val textAnimationEnabled: Flow<Boolean> = context.dataStore.data.map { it[TEXT_ANIMATION_ENABLED] ?: true }")

func = """    suspend fun setTextAnimation(value: String) {
        context.dataStore.edit { it[TEXT_ANIMATION] = value }
    }"""
func_new = """    suspend fun setTextAnimation(value: String) {
        context.dataStore.edit { it[TEXT_ANIMATION] = value }
    }
    
    suspend fun setTextAnimationEnabled(enabled: Boolean) {
        context.dataStore.edit { it[TEXT_ANIMATION_ENABLED] = enabled }
    }"""
sm = sm.replace(func, func_new)

with open("app/src/main/java/com/example/settings/SettingsManager.kt", "w") as f:
    f.write(sm)
