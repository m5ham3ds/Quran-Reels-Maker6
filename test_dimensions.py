import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "arabicTextX" in line and "Offset" in line:
        print(f"L{i}: {line.strip()}")
    if "scalePx" in line and "arabicText" in line:
        print(f"L{i}: {line.strip()}")

