import re

for fname in ["app/src/main/java/com/example/MainActivity.kt", "app/src/main/java/com/example/ui/VideoEditorScreen.kt"]:
    with open(fname, "r") as f:
        content = f.read()

    # Arabic
    content = content.replace("arabicTextY - 90f", "arabicTextY - 160f")
    # Translation
    content = content.replace("translationTextY - 115f", "translationTextY - 225f")
    # Surah Name
    content = content.replace("surahNameY + 180f", "surahNameY + 110f")
    # Qibla Icon
    content = content.replace("iconY + 45f", "iconY + 95f")
    
    with open(fname, "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "r") as f:
    vg = f.read()

# Arabic
vg = vg.replace("arabicTextY.toFloat() - 90f", "arabicTextY.toFloat() - 160f")
# Translation
vg = vg.replace("translationTextY.toFloat() - 115f", "translationTextY.toFloat() - 225f")
# Surah Name
vg = vg.replace("180f + (surahNameY.toFloat())", "110f + (surahNameY.toFloat())")
# Qibla Icon
vg = vg.replace("iconY.toFloat() + 45f", "iconY.toFloat() + 95f")

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "w") as f:
    f.write(vg)

with open("app/src/main/java/com/example/settings/SettingsManager.kt", "r") as f:
    sm = f.read()

sm = sm.replace("it[ICON_SIZE] ?: 20", "it[ICON_SIZE] ?: 40")

with open("app/src/main/java/com/example/settings/SettingsManager.kt", "w") as f:
    f.write(sm)
