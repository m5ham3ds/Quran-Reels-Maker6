with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "spFromCanvas" in line:
        print(f"L{i}: {line.strip()}")
    if "IntOffset" in line:
        print(f"L{i}: {line.strip()}")

