import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

old_padding = """        val horizontalPadding = (48).toInt()
        val textWidth = videoWidth - horizontalPadding"""
new_padding = """        val horizontalPadding = (96f * scaleRatio).toInt()
        val textWidth = videoWidth - horizontalPadding"""
content = content.replace(old_padding, new_padding)

old_start_y = """        val baseStartY = when (textPosition) {
            "Top" -> 100f
            "Bottom" -> videoHeight.toFloat() - totalHeight - 100f
            else -> (videoHeight.toFloat() - totalHeight) / 2f + 150f
        }
        val startY = baseStartY + ((arabicTextY.toFloat() - 70f))"""
        
new_start_y = """        val baseStartY = when (textPosition) {
            "Top" -> 100f * scaleRatio
            "Bottom" -> videoHeight.toFloat() - totalHeight - 100f * scaleRatio
            else -> (videoHeight.toFloat() - totalHeight) / 2f + 150f * scaleRatio
        }
        val startY = baseStartY + (scaledArabicTextY - 70f * scaleRatio)"""
content = content.replace(old_start_y, new_start_y)

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)

