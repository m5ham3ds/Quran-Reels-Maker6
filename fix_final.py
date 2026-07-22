import re

for fname in ["app/src/main/java/com/example/MainActivity.kt", "app/src/main/java/com/example/ui/VideoEditorScreen.kt"]:
    with open(fname, "r") as f:
        content = f.read()

    # Revert Icon to Center
    # First find BottomCenter... -200f
    icon_target = """                .align(Alignment.BottomCenter)
                .size((iconSize * scale).dp)
                .offset(x = (iconX * scale).dp, y = ((iconY - 200f) * scale).dp)"""
    icon_replace = """                .align(Alignment.Center)
                .size((iconSize * scale).dp)
                .offset(x = (iconX * scale).dp, y = ((iconY + 45f) * scale).dp)"""
    
    if icon_target in content:
        content = content.replace(icon_target, icon_replace)
    
    # For VideoEditorScreen, it has scalePx instead of scale
    icon_target_2 = """                        .align(Alignment.BottomCenter)
                        .offset { IntOffset((iconX * scalePx).roundToInt(), ((iconY - 200f) * scalePx).roundToInt()) }"""
    icon_replace_2 = """                        .align(Alignment.Center)
                        .offset { IntOffset((iconX * scalePx).roundToInt(), ((iconY + 45f) * scalePx).roundToInt()) }"""
                        
    if icon_target_2 in content:
        content = content.replace(icon_target_2, icon_replace_2)
        
    with open(fname, "w") as f:
        f.write(content)


with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "r") as f:
    vg = f.read()

# Fix Surah Name Y in VideoGenerator
vg = vg.replace("val surahTopY = 40f + (surahNameY.toFloat())", "val surahTopY = 180f + (surahNameY.toFloat())")

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "w") as f:
    f.write(vg)
