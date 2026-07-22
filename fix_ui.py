import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# 1. Surah Name Y offset
content = content.replace(
    "((surahNameY - 30f) * scalePx)",
    "((surahNameY + 40f) * scalePx)"
)

# 2. Arabic Text Y offset
content = content.replace(
    "((arabicTextY - 140f) * scalePx)",
    "((arabicTextY - 70f) * scalePx)"
)

# 3. Translation Text Y offset
content = content.replace(
    "((translationTextY - 200f) * scalePx)",
    "((translationTextY - 90f) * scalePx)"
)

# 4. Icon Y offset
content = content.replace(
    "((iconY + 120f) * scalePx)",
    "((iconY + 70f) * scalePx)"
)

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
