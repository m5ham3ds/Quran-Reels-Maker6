import re

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'r') as f:
    content = f.read()

content = content.replace("context.dataStore.data.map { it[FONT_SIZE] ?: 40 }", "context.dataStore.data.map { it[FONT_SIZE] ?: 20 }")
content = content.replace("context.dataStore.data.map { it[TRANSLATION_FONT_SIZE] ?: 16 }", "context.dataStore.data.map { it[TRANSLATION_FONT_SIZE] ?: 8 }")
content = content.replace("context.dataStore.data.map { it[SURAH_NAME_FONT_SIZE] ?: 40 }", "context.dataStore.data.map { it[SURAH_NAME_FONT_SIZE] ?: 20 }")
content = content.replace("context.dataStore.data.map { it[ICON_SIZE] ?: 80 }", "context.dataStore.data.map { it[ICON_SIZE] ?: 40 }")

with open('app/src/main/java/com/example/settings/SettingsManager.kt', 'w') as f:
    f.write(content)
