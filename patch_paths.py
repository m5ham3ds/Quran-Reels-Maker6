import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

old_save = """            if (isPreviewMode) {
                uri = Uri.fromFile(File(context.cacheDir, "playable_reel.mp4"))
            } else {
                // Save using MediaStore (Standard and reliable on modern Android)
                try {
                    val values = ContentValues().apply {
                        put(MediaStore.Video.Media.DISPLAY_NAME, "Quran_Reel_${System.currentTimeMillis()}.mp4")
                        put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
                        put(MediaStore.Video.Media.RELATIVE_PATH, "Movies/Quran Reels")
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                            put(MediaStore.Video.Media.IS_PENDING, 1)
                        }
                    }
                    val mUri = context.contentResolver.insert(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, values)
                    if (mUri != null) {
                        context.contentResolver.openOutputStream(mUri)?.use { out ->
                            File(outputPath).inputStream().use { input ->
                                input.copyTo(out)
                            }
                        }
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                            values.clear()
                            values.put(MediaStore.Video.Media.IS_PENDING, 0)
                            context.contentResolver.update(mUri, values, null, null)
                        }
                        uri = mUri
                    }
                } catch (e: Exception) {
                    com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
                }
            } // Close the else branch for isPreviewMode"""

new_save = """            if (isPreviewMode) {
                uri = Uri.fromFile(File(context.cacheDir, "playable_reel.mp4"))
            } else {
                // Save directly to /storage/emulated/0/Movies/Quran Reels as requested
                try {
                    val moviesDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES)
                    val quranReelsDir = File(moviesDir, "Quran Reels")
                    if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
                    val finalFile = File(quranReelsDir, "Quran_Reel_${System.currentTimeMillis()}.mp4")
                    File(outputPath).copyTo(finalFile, overwrite = true)
                    uri = Uri.fromFile(finalFile)
                    
                    // Scan the file so it appears in the gallery
                    android.media.MediaScannerConnection.scanFile(context, arrayOf(finalFile.absolutePath), arrayOf("video/mp4"), null)
                } catch (e: Exception) {
                    com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught saving video: ${ e.message }", e)
                }
            }"""

if old_save in content:
    content = content.replace(old_save, new_save)
    with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
        f.write(content)
    print("Patched VideoGenerator save successfully")
else:
    print("Could not find old_save in VideoGenerator")

