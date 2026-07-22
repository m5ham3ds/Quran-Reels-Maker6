import re
for fname in ["app/src/main/java/com/example/MainActivity.kt", "app/src/main/java/com/example/ui/VideoEditorScreen.kt"]:
    with open(fname, "r") as f:
        content = f.read()
    content = content.replace("val padTop = 30f *", "val padTop = 42f *")
    content = content.replace("val padBottom = 30f *", "val padBottom = 42f *")
    with open(fname, "w") as f:
        f.write(content)
