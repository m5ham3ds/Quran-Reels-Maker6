import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Fix VideoEditorScreen text sizes and offsets
# fontSize = spFromCanvas(fontSize.toFloat() * 2f) -> Wait, I replaced it before.
# Let's check what it has currently.

