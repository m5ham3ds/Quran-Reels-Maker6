with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("val scale = maxWidth.value / 720f\n        val fontScale", "val scale = maxWidth.value / 720f\n        val density = androidx.compose.ui.platform.LocalDensity.current.density\n        val fontScale")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
