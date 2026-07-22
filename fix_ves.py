import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 470 and "val actualWidthDp = minOf(maxWidth, maxHeight * (9f / 16f))" in line:
        continue # skip
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.writelines(new_lines)
