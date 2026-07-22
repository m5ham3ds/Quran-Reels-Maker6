import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix font sizes (remove * 2.1f, etc.)
content = re.sub(r'\(fontSize \* scale(?: \* [\d\.]+f)? / fontScale\)\.sp', r'(fontSize * scale / fontScale).sp', content)
content = re.sub(r'\(surahNameFontSize \* scale(?: \* [\d\.]+f)? / fontScale\)\.sp', r'(surahNameFontSize * scale / fontScale).sp', content)
content = re.sub(r'\(translationFontSize \* scale(?: \* [\d\.]+f)? / fontScale\)\.sp', r'(translationFontSize * scale / fontScale).sp', content)

# Fix icon size
content = re.sub(r'\(iconSize \* scale(?: \* [\d\.]+f)?\)\.dp', r'(iconSize * scale).dp', content)

# Fix offsets
content = re.sub(r'arabicTextX \* scale(?: \* 2f)?', r'arabicTextX * scale', content)
content = re.sub(r'arabicTextY \* scale(?: \* 2f)? - 90f \* scale(?: \* 2f)?', r'(arabicTextY - 90f) * scale', content)

content = re.sub(r'translationTextX \* scale(?: \* 2f)?', r'translationTextX * scale', content)
content = re.sub(r'translationTextY \* scale(?: \* 2f)? - 115f \* scale(?: \* 2f)?', r'(translationTextY - 115f) * scale', content)

content = re.sub(r'surahNameX \* scale(?: \* 2f)?', r'surahNameX * scale', content)
content = re.sub(r'surahNameY \* scale(?: \* 2f)?', r'(surahNameY + 40f) * scale', content)
# Wait, in VideoGenerator, surahTopY is 40f + surahNameY.toFloat().
# So it should be (surahNameY + 40f) * scale.
# Let's fix MainActivity.kt to just use (surahNameY + 40f) * scale.

content = re.sub(r'iconX \* scale(?: \* 2f)?', r'iconX * scale', content)
content = re.sub(r'iconY \* scale(?: \+ 45f \* scale)?(?: \* 2f)?', r'(iconY + 45f) * scale', content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

