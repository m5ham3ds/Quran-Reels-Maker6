import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

content = content.replace("val boxPadding = 30f", "val boxPadding = 30f * scaleRatio")
content = content.replace("val boxHeight = totalHeight + (84f)", "val boxHeight = totalHeight + (84f * scaleRatio)")
content = content.replace("val boxTop = baseStartY - (42f)", "val boxTop = baseStartY - (42f * scaleRatio)")
content = content.replace("val transY = baseStartY + sl.height + 32f + ((translationTextY.toFloat() - 110f))", "val transY = baseStartY + sl.height + 32f * scaleRatio + (scaledTranslationTextY - 110f * scaleRatio)")
content = content.replace("val heartY = videoHeight / 2f + (iconY.toFloat() + 50f + 95f) - iconPaint.descent()", "val heartY = videoHeight / 2f + (scaledIconY + 50f * scaleRatio + 95f * scaleRatio) - iconPaint.descent()")
content = content.replace("val totalHeight = sl.height + (transSl?.height?.plus(32f) ?: 0f)", "val totalHeight = sl.height + (transSl?.height?.plus(32f * scaleRatio) ?: 0f)")

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)

