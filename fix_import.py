with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "import androidx.compose.ui.draw.drawBehind":
        continue
    new_lines.append(line)

new_lines.insert(2, "import androidx.compose.ui.draw.drawBehind\n")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(new_lines)
