import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

idx = content.find('createVerseBitmap(')
end_idx = content.find('drainEncoder', idx)
print(content[idx:end_idx+200])

