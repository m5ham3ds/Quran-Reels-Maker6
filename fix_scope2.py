import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    v = f.read()

target = """    val pexelsApiKey by settingsManager.pexelsApiKey.collectAsState(initial = "")
    val bgTransitionEnabled by settingsManager.bgTransitionEnabled.collectAsState(initial = false)
    val bgTransitionType by settingsManager.bgTransitionType.collectAsState(initial = "dissolve")"""

replacement = """    val pexelsApiKey by settingsManager.pexelsApiKey.collectAsState(initial = "")"""

v = v.replace(target, replacement)

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(v)
