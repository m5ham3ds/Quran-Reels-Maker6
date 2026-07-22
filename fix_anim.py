import re

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "r") as f:
    vg = f.read()

target = """        var animScale = 1f
        var animTranslateY = 0f
        
        if (chunkTimeMs < animDuration && chunkTimeMs >= 0L) {
            val progress = chunkTimeMs.toFloat() / animDuration.toFloat()
            val easeOut = 1f - Math.pow((1f - progress).toDouble(), 3.0).toFloat()
            when (textAnimationType) {
                "Fade" -> {
                    animAlpha = easeOut
                }
                "SlideUp" -> {
                    animAlpha = easeOut
                    animTranslateY = 40f * (1f - easeOut)
                }
                "Scale" -> {
                    animAlpha = easeOut
                    animScale = 0.85f + (0.15f * easeOut)
                }
            }
        }"""

replacement = """        var animScale = 1f
        var animTranslateY = 0f
        var animTranslateX = 0f
        
        if (textAnimationEnabled && chunkTimeMs < animDuration && chunkTimeMs >= 0L) {
            val progress = chunkTimeMs.toFloat() / animDuration.toFloat()
            val easeOut = 1f - Math.pow((1f - progress).toDouble(), 3.0).toFloat()
            when (textAnimationType) {
                "Fade" -> {
                    animAlpha = easeOut
                }
                "SlideUp" -> {
                    animAlpha = easeOut
                    animTranslateY = 40f * (1f - easeOut)
                }
                "SlideRight" -> {
                    animAlpha = easeOut
                    animTranslateX = -40f * (1f - easeOut)
                }
                "Scale" -> {
                    animAlpha = easeOut
                    animScale = 0.85f + (0.15f * easeOut)
                }
            }
        }"""

if target in vg:
    vg = vg.replace(target, replacement)
    print("Replaced animation block")
else:
    print("Animation block not found")

target_canvas = """        canvas.save()
        if (animScale != 1f || animTranslateY != 0f) {
            val pivotX = videoWidth / 2f
            val pivotY = baseStartY + (totalHeight / 2f)
            canvas.translate(0f, animTranslateY)
            canvas.scale(animScale, animScale, pivotX, pivotY)
        }"""

replacement_canvas = """        canvas.save()
        if (animScale != 1f || animTranslateY != 0f || animTranslateX != 0f) {
            val pivotX = videoWidth / 2f
            val pivotY = baseStartY + (totalHeight / 2f)
            canvas.translate(animTranslateX, animTranslateY)
            canvas.scale(animScale, animScale, pivotX, pivotY)
        }"""

if target_canvas in vg:
    vg = vg.replace(target_canvas, replacement_canvas)
    print("Replaced canvas block")
else:
    print("Canvas block not found")

with open("app/src/main/java/com/example/generator/VideoGenerator.kt", "w") as f:
    f.write(vg)
