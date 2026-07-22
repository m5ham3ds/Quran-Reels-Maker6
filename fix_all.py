import os

# 1. Fix VideoGenerator.kt baselines and transition logic
vg_path = "app/src/main/java/com/example/generator/VideoGenerator.kt"
with open(vg_path, "r") as f:
    vg_content = f.read()

# Fix baselines
vg_content = vg_content.replace("arabicTextY.toFloat() - 160f", "arabicTextY.toFloat()")
vg_content = vg_content.replace("translationTextY.toFloat() - 225f", "translationTextY.toFloat()")

# Fix transition logic: Move decoder and lastVideoIdx outside the loop
target_str = """            var previousVideoLastFrame: Bitmap? = null
            var currentBgFrameForTransition: Bitmap? = null
            
            val reusableVerseBitmap = Bitmap.createBitmap(vidWidth, vidHeight, Bitmap.Config.ARGB_8888)
            val reusableCanvas = Canvas(reusableVerseBitmap)
            var reusableArgb: IntArray? = null
            for ((idx, verse) in verses.withIndex()) {
                reportProgress(if (isArabic) "جاري تصوير مشهدي الآية ${startAyah + idx}..." else "Rendering scenes for Ayah ${startAyah + idx}...", 0.5f + (idx * 0.4f / verses.size))
                
                var frameDecoder: SequentialFrameDecoder? = null
                var lastVideoIdx = -1"""

replacement_str = """            var previousVideoLastFrame: Bitmap? = null
            var currentBgFrameForTransition: Bitmap? = null
            
            var frameDecoder: SequentialFrameDecoder? = null
            var lastVideoIdx = -1
            
            val reusableVerseBitmap = Bitmap.createBitmap(vidWidth, vidHeight, Bitmap.Config.ARGB_8888)
            val reusableCanvas = Canvas(reusableVerseBitmap)
            var reusableArgb: IntArray? = null
            for ((idx, verse) in verses.withIndex()) {
                reportProgress(if (isArabic) "جاري تصوير مشهدي الآية ${startAyah + idx}..." else "Rendering scenes for Ayah ${startAyah + idx}...", 0.5f + (idx * 0.4f / verses.size))"""

vg_content = vg_content.replace(target_str, replacement_str)

# Fix chunk size counting for background index
vg_content = vg_content.replace("val globalChunkOffset = verses.take(idx).sumOf { it.chunks.size }", "val globalChunkOffset = verses.take(idx).sumOf { it.chunks.size.coerceAtLeast(1) }")

# Release frame decoder at the end
release_target = """            previousVideoLastFrame?.recycle()
            currentBgFrameForTransition?.recycle()
            reusableVerseBitmap.recycle()"""

release_replacement = """            frameDecoder?.release()
            previousVideoLastFrame?.recycle()
            currentBgFrameForTransition?.recycle()
            reusableVerseBitmap.recycle()"""

vg_content = vg_content.replace(release_target, release_replacement)

with open(vg_path, "w") as f:
    f.write(vg_content)

# 2. Fix VideoEditorScreen.kt baselines
ve_path = "app/src/main/java/com/example/ui/VideoEditorScreen.kt"
with open(ve_path, "r") as f:
    ve_content = f.read()

ve_content = ve_content.replace("arabicTextY - 160f", "arabicTextY")
ve_content = ve_content.replace("translationTextY - 225f", "translationTextY")

with open(ve_path, "w") as f:
    f.write(ve_content)
