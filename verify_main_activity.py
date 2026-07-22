with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "fontSize = (" in line:
        print(f"L{i}: {line.strip()}")
    if ".offset(x = (" in line:
        print(f"L{i}: {line.strip()}")
    if "surahNameFontSize =" in line:
        print(f"L{i}: {line.strip()}")

