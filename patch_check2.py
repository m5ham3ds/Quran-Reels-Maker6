import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

idx = content.find('createVerseBitmap(')
end_idx = content.find('fun createVerseBitmap', idx)
print(content[idx:idx+1500])

