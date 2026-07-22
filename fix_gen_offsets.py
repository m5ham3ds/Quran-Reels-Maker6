import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

# Fix totalHeight
content = content.replace(
    'val totalHeight = sl.height + (transSl?.height ?: 0)',
    'val totalHeight = sl.height + (transSl?.height?.plus(32f * scaleRatio) ?: 0f)'
)

# Fix baseStartY
content = content.replace(
    'else -> (videoHeight.toFloat() - totalHeight) / 2f + 150f * scaleRatio',
    'else -> (videoHeight.toFloat() - totalHeight) / 2f'
)

# Fix startY
content = content.replace(
    'val startY = baseStartY + (scaledArabicTextY - 70f * scaleRatio)',
    'val startY = baseStartY + scaledArabicTextY'
)

# Fix transY
content = content.replace(
    'val transY = baseStartY + sl.height + (scaledTranslationTextY - 90f * scaleRatio)',
    'val transY = baseStartY + sl.height + 32f * scaleRatio + scaledTranslationTextY'
)

# Fix surahTopY
content = content.replace(
    'val surahTopY = 40f * scaleRatio + scaledSurahNameY',
    'val surahTopY = scaledSurahNameY'
)

# Fix heartY
content = content.replace(
    'val heartY = videoHeight / 2f + (scaledIconY + 70f * scaleRatio) - iconPaint.descent()',
    'val heartY = videoHeight / 2f + scaledIconY - iconPaint.descent()'
)

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)
