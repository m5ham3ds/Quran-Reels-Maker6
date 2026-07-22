import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

content = content.replace("scaledTextFontSize.toInt()", "textFontSize")
content = content.replace("scaledTranslationFontSize.toInt()", "translationFontSize")

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)

