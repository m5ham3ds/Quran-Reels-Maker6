import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'var translationFontSize by remember { mutableFloatStateOf(8f) }',
    'var translationFontSize by remember { mutableFloatStateOf(8f) }\n    var surahNameFontSize by remember { mutableFloatStateOf(44f) }'
)

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)

