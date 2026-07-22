import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

save_fn = """    fun savePosition(element: String, x: Float, y: Float) {
        // Do not modify global defaults during preview.
    }"""

new_save_fn = """    fun savePosition(element: String, x: Float, y: Float) {
        coroutineScope.launch {
            when (element) {
                "arabic" -> { settingsManager.setArabicTextX(x.toInt()); settingsManager.setArabicTextY(y.toInt()) }
                "translation" -> { settingsManager.setTranslationTextX(x.toInt()); settingsManager.setTranslationTextY(y.toInt()) }
                "surah" -> { settingsManager.setSurahNameX(x.toInt()); settingsManager.setSurahNameY(y.toInt()) }
                "icon" -> { settingsManager.setIconX(x.toInt()); settingsManager.setIconY(y.toInt()) }
            }
        }
    }"""

content = content.replace(save_fn, new_save_fn)

# Add LaunchedEffects for the sizes/opacities
launched_effects = """    LaunchedEffect(fontSize) { settingsManager.setFontSize(fontSize.toInt()) }
    LaunchedEffect(translationFontSize) { settingsManager.setTranslationFontSize(translationFontSize.toInt()) }
    LaunchedEffect(surahNameFontSize) { settingsManager.setSurahNameFontSize(surahNameFontSize.toInt()) }
    LaunchedEffect(iconSize) { settingsManager.setIconSize(iconSize.toInt()) }
    
    LaunchedEffect(textOpacity) { settingsManager.setTextOpacity(textOpacity) }
    LaunchedEffect(translationOpacity) { settingsManager.setTranslationOpacity(translationOpacity) }
    LaunchedEffect(surahNameOpacity) { settingsManager.setSurahNameOpacity(surahNameOpacity) }
    LaunchedEffect(iconOpacity) { settingsManager.setIconOpacity(iconOpacity) }
    
    LaunchedEffect(textColor) { settingsManager.setTextColor(textColor) }
    LaunchedEffect(quranFontFamily) { settingsManager.setFontFamily(quranFontFamily) }
    LaunchedEffect(surahNameFontFamily) { settingsManager.setSurahNameFontFamily(surahNameFontFamily) }
    LaunchedEffect(translationFontFamily) { settingsManager.setTranslationFontFamily(translationFontFamily) }
    
    LaunchedEffect(textAlignStr) { settingsManager.setTextAlign(textAlignStr) }
"""

# Insert right after variables are declared and settings are loaded.
# Look for: "LaunchedEffect(Unit) {"
content = content.replace("    LaunchedEffect(Unit) {", launched_effects + "\n    LaunchedEffect(Unit) {")

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
