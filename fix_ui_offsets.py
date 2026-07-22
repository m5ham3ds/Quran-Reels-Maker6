import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Fix Column textPosition offset
content = content.replace(
    'else -> IntOffset(0, (150f * scalePx).roundToInt())',
    'else -> IntOffset(0, 0)'
)

# Fix offsets
content = content.replace(
    '(((arabicTextY - 70f)) * scalePx)',
    '(arabicTextY * scalePx)'
)
content = content.replace(
    '(((translationTextY - 90f)) * scalePx)',
    '(translationTextY * scalePx)'
)
content = content.replace(
    '((surahNameY + 40f) * scalePx)',
    '(surahNameY * scalePx)'
)
content = content.replace(
    '((iconY + 70f) * scalePx)',
    '(iconY * scalePx)'
)

# Load font sizes and opacities in LaunchedEffect
load_code = """
                                arabicTextX = settingsManager.arabicTextX.first().toFloat()
                                arabicTextY = settingsManager.arabicTextY.first().toFloat()
                                translationTextX = settingsManager.translationTextX.first().toFloat()
                                translationTextY = settingsManager.translationTextY.first().toFloat()
                                surahNameX = settingsManager.surahNameX.first().toFloat()
                                surahNameY = settingsManager.surahNameY.first().toFloat()
                                iconX = settingsManager.iconX.first().toFloat()
                                iconY = settingsManager.iconY.first().toFloat()
                                
                                fontSize = settingsManager.fontSize.first().toFloat()
                                translationFontSize = settingsManager.translationFontSize.first().toFloat()
                                surahNameFontSize = settingsManager.surahNameFontSize.first().toFloat()
                                iconSize = settingsManager.iconSize.first().toFloat()
                                
                                textOpacity = settingsManager.textOpacity.first()
                                translationOpacity = settingsManager.translationOpacity.first()
                                surahNameOpacity = settingsManager.surahNameOpacity.first()
                                iconOpacity = settingsManager.iconOpacity.first()
"""
content = re.sub(r'(\s+)arabicTextX = settingsManager\.arabicTextX\.first\(\)\.toFloat\(\)[\s\S]*?iconY = settingsManager\.iconY\.first\(\)\.toFloat\(\)', load_code, content)

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
