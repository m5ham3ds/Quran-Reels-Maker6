import re

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "r") as f:
    content = f.read()

content = content.replace("((iconY.toFloat() + 45f) * 2f)", "(iconY.toFloat() + 45f)")
content = content.replace("(iconX.toFloat() * 2f)", "(iconX.toFloat())")

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "w") as f:
    f.write(content)

