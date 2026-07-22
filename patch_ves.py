import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Add surahNameFontSize
content = re.sub(
    r'(var translationFontSize by remember \{ mutableFloatStateOf\(20f\) \})',
    r'\1\n    var surahNameFontSize by remember { mutableFloatStateOf(44f) }',
    content
)

content = re.sub(
    r'(translationFontSize = settingsManager\.translationFontSize\.first\(\)\.toFloat\(\))',
    r'\1\n        surahNameFontSize = settingsManager.surahNameFontSize.first().toFloat()',
    content
)

content = re.sub(
    r'(val transFontSize: Float)',
    r'\1,\n        val surahNameFontSize: Float',
    content
)

content = re.sub(
    r'(fontSize, translationFontSize, textColor)',
    r'fontSize, translationFontSize, surahNameFontSize, textColor',
    content
)

content = re.sub(
    r'(translationFontSize = state\.transFontSize)',
    r'\1\n        surahNameFontSize = state.surahNameFontSize',
    content
)

# Use it
content = content.replace("fontSize = spFromCanvas(24f),", "fontSize = spFromCanvas(surahNameFontSize),")

# Surah offset: video generator has `val surahTopY = 40f + surahNameY.toFloat()`
# So it should be `surahNameY + 40f` in VideoEditorScreen.
content = content.replace("IntOffset((surahNameX * scalePx).roundToInt(), (surahNameY * scalePx).roundToInt())", "IntOffset((surahNameX * scalePx).roundToInt(), ((surahNameY + 40f) * scalePx).roundToInt())")


with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)

