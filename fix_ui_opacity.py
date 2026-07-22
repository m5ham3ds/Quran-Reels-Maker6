import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("var surahNameOpacity by remember { mutableFloatStateOf(1f) }", "var surahNameOpacity by remember { mutableFloatStateOf(0.8f) }")
content = content.replace("var translationOpacity by remember { mutableFloatStateOf(1f) }", "var translationOpacity by remember { mutableFloatStateOf(0.8f) }")
content = content.replace("var textOpacity by remember { mutableFloatStateOf(1f) }", "var textOpacity by remember { mutableFloatStateOf(0.8f) }")

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
