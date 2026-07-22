import re

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'r') as f:
    content = f.read()

content = content.replace("val arabicTextY: Flow<Int> = context.dataStore.data.map { it[ARABIC_TEXT_Y] ?: 0 }", "val arabicTextY: Flow<Int> = context.dataStore.data.map { it[ARABIC_TEXT_Y] ?: -70 }")
content = content.replace("val translationTextY: Flow<Int> = context.dataStore.data.map { it[TRANSLATION_TEXT_Y] ?: 0 }", "val translationTextY: Flow<Int> = context.dataStore.data.map { it[TRANSLATION_TEXT_Y] ?: -90 }")
content = content.replace("val surahNameY: Flow<Int> = context.dataStore.data.map { it[SURAH_NAME_Y] ?: 0 }", "val surahNameY: Flow<Int> = context.dataStore.data.map { it[SURAH_NAME_Y] ?: 40 }")
content = content.replace("val iconY: Flow<Int> = context.dataStore.data.map { it[ICON_Y] ?: 0 }", "val iconY: Flow<Int> = context.dataStore.data.map { it[ICON_Y] ?: 70 }")

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'w') as f:
    f.write(content)
