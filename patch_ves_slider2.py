import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

content = content.replace('selectedElement == "surah_name"', 'selectedElement == "surah"')

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)

