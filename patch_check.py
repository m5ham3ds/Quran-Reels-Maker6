import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

idx = content.find('fun createVerseBitmap')
print(content[idx:idx+2000])

