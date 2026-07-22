import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

idx = content.find('fun fillImageFromBitmap')
end_idx = content.find('fun getActiveSmartChunk', idx)
print(content[idx:end_idx])

