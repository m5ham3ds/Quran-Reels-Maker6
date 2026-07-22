import re
with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    c = f.read()
target = """                },
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {"""
replace = """                },
                verticalArrangement = Arrangement.spacedBy(dpFromCanvas(32f))
            ) {"""
if target in c:
    c = c.replace(target, replace)
with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(c)
