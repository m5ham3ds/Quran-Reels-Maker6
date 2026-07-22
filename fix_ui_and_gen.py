import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Fix Editor Offsets
content = content.replace("surahNameY - 40f", "surahNameY - 30f")
content = content.replace("arabicTextY - 160f", "arabicTextY - 140f")
content = content.replace("translationTextY - 230f", "translationTextY - 200f")
content = content.replace("iconY + 120f", "iconY + 120f") # Remains the same, but just in case it was different

# Ensure sizes are correct in state
content = content.replace("var surahNameFontSize by remember { mutableFloatStateOf(44f) }", "var surahNameFontSize by remember { mutableFloatStateOf(20f) }")
content = content.replace("var iconSize by remember { mutableFloatStateOf(20f) }", "var iconSize by remember { mutableFloatStateOf(40f) }")

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    gen_content = f.read()

# Fix Generator Offsets
gen_content = gen_content.replace("140f * scaleRatio + scaledSurahNameY", "150f * scaleRatio + scaledSurahNameY") # Surah Name: old 110 + 40 = 150
gen_content = gen_content.replace("scaledArabicTextY - 160f * scaleRatio", "scaledArabicTextY - 140f * scaleRatio")
gen_content = gen_content.replace("scaledTranslationTextY - 230f * scaleRatio", "scaledTranslationTextY - 200f * scaleRatio")
gen_content = gen_content.replace("scaledIconY + 120f * scaleRatio", "scaledIconY + 120f * scaleRatio") # Icon: old 50 + 70 = 120

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(gen_content)

