import sys

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

# 1. Update vidWidth, vidHeight, vidBitrate
old_vid_block = """            var vidWidth = 720
            var vidHeight = 1280
            var vidBitrate = 4000000"""

new_vid_block = """            var vidWidth = 720
            var vidHeight = 1280
            var vidBitrate = 4000000
            
            when (videoQuality) {
                "Ultra" -> {
                    vidWidth = 1080
                    vidHeight = 1920
                    vidBitrate = 16000000
                }
                "High" -> {
                    vidWidth = 1080
                    vidHeight = 1920
                    vidBitrate = 8000000
                }
                "Normal" -> {
                    vidWidth = 720
                    vidHeight = 1280
                    vidBitrate = 4000000
                }
            }"""
content = content.replace(old_vid_block, new_vid_block)

# 2. Add scaleRatio to createVerseBitmap
create_verse_start = content.find("fun createVerseBitmap(")
create_verse_body_start = content.find("bitmap.eraseColor(Color.TRANSPARENT)", create_verse_start)

scale_ratio_code = """
        val scaleRatio = videoWidth / 720f
        val scaledTextFontSize = textFontSize.toFloat() * scaleRatio
        val scaledTranslationFontSize = translationFontSize.toFloat() * scaleRatio
        val scaledSurahNameFontSize = surahNameFontSize.toFloat() * scaleRatio
        val scaledIconSize = iconSize.toFloat() * scaleRatio
        val scaledArabicTextX = arabicTextX.toFloat() * scaleRatio
        val scaledArabicTextY = arabicTextY.toFloat() * scaleRatio
        val scaledTranslationTextX = translationTextX.toFloat() * scaleRatio
        val scaledTranslationTextY = translationTextY.toFloat() * scaleRatio
        val scaledSurahNameX = surahNameX.toFloat() * scaleRatio
        val scaledSurahNameY = surahNameY.toFloat() * scaleRatio
        val scaledIconX = iconX.toFloat() * scaleRatio
        val scaledIconY = iconY.toFloat() * scaleRatio
        val scaledTextBgRadius = textBgRadius.toFloat() * scaleRatio
        
"""
content = content[:create_verse_body_start] + scale_ratio_code + content[create_verse_body_start:]

# 3. Replace parameters in createVerseBitmap with scaled ones
content = content.replace("surahNameFontSize.toFloat()", "scaledSurahNameFontSize")
content = content.replace("(surahNameX.toFloat())", "scaledSurahNameX")
content = content.replace("(surahNameY.toFloat())", "scaledSurahNameY")
content = content.replace("textFontSize.toFloat()", "scaledTextFontSize")
content = content.replace("textFontSize", "scaledTextFontSize.toInt()")  # For any direct use of int, wait, let's just replace all
content = content.replace("translationFontSize.toFloat()", "scaledTranslationFontSize")
content = content.replace("translationFontSize", "scaledTranslationFontSize.toInt()")

content = content.replace("(arabicTextX.toFloat())", "scaledArabicTextX")
content = content.replace("(arabicTextY.toFloat())", "scaledArabicTextY")

content = content.replace("(translationTextX.toFloat())", "scaledTranslationTextX")
content = content.replace("(translationTextY.toFloat())", "scaledTranslationTextY")

content = content.replace("iconSize.toFloat()", "scaledIconSize")
content = content.replace("(iconX.toFloat())", "scaledIconX")
content = content.replace("(iconY.toFloat())", "scaledIconY")

content = content.replace("textBgRadius.toFloat()", "scaledTextBgRadius")

# Also fix the constants 110f, 150f, etc.
content = content.replace("val surahTopY = 110f +", "val surahTopY = 110f * scaleRatio +")
content = content.replace("val baseY = videoHeight / 2f + (150f * scaleRatio)", "val baseY = videoHeight / 2f + (150f * scaleRatio)") # We will regex this safely

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)

