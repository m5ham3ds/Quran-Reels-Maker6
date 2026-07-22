import re

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "r") as f:
    vg = f.read()

vg = vg.replace(
    "val textAnimationType = settingsManager.textAnimation.first()",
    "val textAnimationType = settingsManager.textAnimation.first()\n            val textAnimationEnabled = settingsManager.textAnimationEnabled.first()"
)

vg = vg.replace(
    "textAnimationType = textAnimationType,",
    "textAnimationEnabled = textAnimationEnabled,\n                        textAnimationType = textAnimationType,"
)

vg = vg.replace(
    "textAlign: String,\n        textAnimationType: String,",
    "textAlign: String,\n        textAnimationEnabled: Boolean,\n        textAnimationType: String,"
)

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "w") as f:
    f.write(vg)
