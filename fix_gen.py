import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

# 1. Fix baseStartY total height calculation (Remove 32f)
content = content.replace(
    "val totalHeight = sl.height + (transSl?.height?.plus(32f * scaleRatio) ?: 0f)",
    "val totalHeight = sl.height + (transSl?.height ?: 0)"
)

# 2. Fix translation layout position and offset
content = content.replace(
    "val transY = baseStartY + sl.height + 32f * scaleRatio + (scaledTranslationTextY - 200f * scaleRatio)",
    "val transY = baseStartY + sl.height + (scaledTranslationTextY - 90f * scaleRatio)"
)

# 3. Fix Arabic offset
content = content.replace(
    "val startY = baseStartY + (scaledArabicTextY - 140f * scaleRatio)",
    "val startY = baseStartY + (scaledArabicTextY - 70f * scaleRatio)"
)

# 4. Fix background box width to match UI (96f padding instead of 60f)
content = content.replace(
    "val boxPadding = 30f * scaleRatio",
    "val boxPadding = 48f * scaleRatio"
)

# 5. Fix Surah offset
content = content.replace(
    "val surahTopY = 150f * scaleRatio + scaledSurahNameY",
    "val surahTopY = 40f * scaleRatio + scaledSurahNameY"
)

# 6. Fix Icon offset
content = content.replace(
    "scaledIconY + 120f * scaleRatio + 95f * scaleRatio",
    "scaledIconY + 70f * scaleRatio"
)

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)
