import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("var surahNameFontSize by remember { mutableFloatStateOf(44f) }", "var surahNameFontSize by remember { mutableFloatStateOf(20f) }")
content = content.replace("var iconSize by remember { mutableFloatStateOf(20f) }", "var iconSize by remember { mutableFloatStateOf(40f) }")

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
