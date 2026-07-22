import re

with open('app/src/main/java/com/example/ui/ReelViewModel.kt', 'r') as f:
    content = f.read()

old_details = """                            var rawSuccess = false
                            try {
                                val values = android.content.ContentValues().apply {
                                    put(android.provider.MediaStore.MediaColumns.DISPLAY_NAME, "Quran_Reel_Publish_Details_${System.currentTimeMillis()}.txt")
                                    put(android.provider.MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                                        put(android.provider.MediaStore.MediaColumns.RELATIVE_PATH, "Movies/Quran Reels/Details")
                                    }
                                }
                                val collection = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                                    android.provider.MediaStore.Files.getContentUri("external")
                                } else {
                                    android.provider.MediaStore.Files.getContentUri("external")
                                }
                                val mUri = app.contentResolver.insert(collection, values)
                                if (mUri != null) {
                                    app.contentResolver.openOutputStream(mUri)?.use { out ->
                                        out.write(detailsContent.toByteArray(Charsets.UTF_8))
                                    }
                                    rawSuccess = true
                                    AppLogger.d("DetailsWriter", "Saved details using MediaStore to Downloads/Quran Reels/Details")
                                }
                            } catch (e: Exception) {
                                AppLogger.e("DetailsWriter", "Raw path write failed: ${e.message}. Using MediaStore insertion...")
                            }

                            // If raw file creation fails (due to Scoped Storage on Android 10+), write using MediaStore ContentResolver!
                            if (!rawSuccess) {
                                val values = android.content.ContentValues().apply {
                                    put(android.provider.MediaStore.MediaColumns.DISPLAY_NAME, "Quran_Reel_Publish_Details_${System.currentTimeMillis()}.txt")
                                    put(android.provider.MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                                        put(android.provider.MediaStore.MediaColumns.RELATIVE_PATH, "Movies/Quran Reels/Details")
                                    }
                                }
                                
                                val externalUri = android.provider.MediaStore.Files.getContentUri("external")
                                val textUri = app.contentResolver.insert(externalUri, values)
                                if (textUri != null) {
                                    app.contentResolver.openOutputStream(textUri)?.use { out ->
                                        out.write(detailsContent.toByteArray(Charsets.UTF_8))
                                    }
                                    AppLogger.d("DetailsWriter", "Saved details to MediaStore database successfully: $textUri")
                                } else {
                                    AppLogger.e("DetailsWriter", "Failed to retrieve MediaStore reference.")
                                }
                            }"""

new_details = """                            try {
                                val moviesDir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES)
                                val detailsDir = java.io.File(moviesDir, "Quran Reels/Details")
                                if (!detailsDir.exists()) detailsDir.mkdirs()
                                
                                // Delete old detail files automatically
                                detailsDir.listFiles()?.forEach { it.delete() }
                                
                                val detailsFile = java.io.File(detailsDir, "Quran_Reel_Publish_Details_${System.currentTimeMillis()}.txt")
                                java.io.FileOutputStream(detailsFile).use { out ->
                                    out.write(detailsContent.toByteArray(Charsets.UTF_8))
                                }
                                AppLogger.d("DetailsWriter", "Saved details directly to ${detailsFile.absolutePath}")
                            } catch (e: Exception) {
                                AppLogger.e("DetailsWriter", "Direct path write failed: ${e.message}", e)
                            }"""

if old_details in content:
    content = content.replace(old_details, new_details)
    with open('app/src/main/java/com/example/ui/ReelViewModel.kt', 'w') as f:
        f.write(content)
    print("Patched ReelViewModel details successfully")
else:
    print("Could not find old_details in ReelViewModel")

