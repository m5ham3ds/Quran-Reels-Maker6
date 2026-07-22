import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    v = f.read()

target = """    val showTranslation by settingsManager.showTranslation.collectAsState(initial = true)"""

replacement = """    val showTranslation by settingsManager.showTranslation.collectAsState(initial = true)
    val bgTransitionEnabled by settingsManager.bgTransitionEnabled.collectAsState(initial = false)
    val bgTransitionType by settingsManager.bgTransitionType.collectAsState(initial = "dissolve")"""

if target in v:
    v = v.replace(target, replacement)
    print("Fixed scope")
else:
    print("Not found")

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(v)
