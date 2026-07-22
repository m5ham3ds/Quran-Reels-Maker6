import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace all arbitrary scaling factors in LivePreviewContainer
# First, remove * 2.3f
content = content.replace("fontSize * scale * 2.3f", "fontSize * scale")
# Then remove * 1.6f
content = content.replace("surahNameFontSize * scale * 1.6f", "surahNameFontSize * scale")
content = content.replace("translationFontSize * scale * 1.6f", "translationFontSize * scale")
content = content.replace("iconSize * scale * 1.6f", "iconSize * scale")

# Remove * 2f for offsets
content = content.replace("arabicTextX * scale * 2f", "arabicTextX * scale")
content = content.replace("arabicTextY * scale * 2f", "arabicTextY * scale")
content = content.replace("translationTextX * scale * 2f", "translationTextX * scale")
content = content.replace("translationTextY * scale * 2f", "translationTextY * scale")
content = content.replace("surahNameX * scale * 2f", "surahNameX * scale")
content = content.replace("surahNameY * scale * 2f", "surahNameY * scale")
content = content.replace("iconX * scale * 2f", "iconX * scale")
content = content.replace("iconY * scale * 2f + 45f * scale * 2f", "iconY * scale + 45f * scale")

# also replace inside modifiers, just in case
content = re.sub(r' \* 2\.3f', '', content)
content = re.sub(r' \* 1\.6f', '', content)
# Wait, * 2f might be used elsewhere. Let's be careful.
# I will only replace the specific ones I found.

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

