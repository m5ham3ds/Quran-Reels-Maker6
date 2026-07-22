import os

files = [
    "app/src/main/java/com/example/generator/VideoGenerator.kt",
    "app/src/main/java/com/example/ui/VideoEditorScreen.kt",
    "app/src/main/java/com/example/MainActivity.kt"
]

for filepath in files:
    with open(filepath, "r") as f:
        content = f.read()

    # In VideoGenerator:
    content = content.replace("arabicTextY.toFloat()", "arabicTextY.toFloat() - 70f")
    content = content.replace("translationTextY.toFloat()", "translationTextY.toFloat() - 110f")
    content = content.replace("surahNameY.toFloat() + 40f", "surahNameY.toFloat() - 70f")
    content = content.replace("iconY.toFloat()", "iconY.toFloat() + 50f")

    # In VideoEditorScreen / MainActivity:
    content = content.replace("arabicTextY * scalePx", "(arabicTextY - 70f) * scalePx")
    content = content.replace("arabicTextY * scale", "(arabicTextY - 70f) * scale")
    
    content = content.replace("translationTextY * scalePx", "(translationTextY - 110f) * scalePx")
    content = content.replace("translationTextY * scale", "(translationTextY - 110f) * scale")
    
    content = content.replace("surahNameY + 110f", "surahNameY - 70f")
    content = content.replace("surahNameY + 40f", "surahNameY - 70f")
    
    content = content.replace("iconY + 95f", "iconY + 50f")
    content = content.replace("iconY * scale", "(iconY + 50f) * scale")

    with open(filepath, "w") as f:
        f.write(content)

