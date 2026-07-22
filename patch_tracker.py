import re

with open('app/src/main/java/com/example/generator/SystemDiagnosticTracker.kt', 'r') as f:
    content = f.read()

old_tracker = """        // 1. Try Public Movies Directory directly
        try {
            val moviesDir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES)
            val quranReelsDir = java.io.File(moviesDir, "Quran Reels/ERROR")
            if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
            val file = java.io.File(quranReelsDir, fileName)
            java.io.PrintWriter(java.io.FileWriter(file)).use { it.print(reportContent) }
            finalPath = file.absolutePath
            com.example.utils.AppLogger.i("SystemDiagnosticTracker", "Report saved via public directory: $finalPath")
            return finalPath
        } catch (e: Exception) {
            com.example.utils.AppLogger.e("SystemDiagnosticTracker", "Failed to save via public directory", e)
        }

        // 2. Try MediaStore fallback
        try {
            val values = android.content.ContentValues().apply {
                put(android.provider.MediaStore.MediaColumns.DISPLAY_NAME, fileName)
                put(android.provider.MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                    put(android.provider.MediaStore.MediaColumns.RELATIVE_PATH, android.os.Environment.DIRECTORY_MOVIES + "/Quran Reels/ERROR")
                }
            }
            val collection = android.provider.MediaStore.Files.getContentUri("external")
            val uri = context.contentResolver.insert(collection, values)
            if (uri != null) {
                context.contentResolver.openOutputStream(uri)?.use { out ->
                    java.io.OutputStreamWriter(out).use { writer ->
                        writer.write(reportContent)
                    }
                }
                finalPath = uri.toString()
                return finalPath
            }
        } catch (e: Exception) {
            com.example.utils.AppLogger.e("SystemDiagnosticTracker", "Failed to save via MediaStore", e)
        }"""

new_tracker = """        // Direct Public Movies Directory as requested
        try {
            val moviesDir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES)
            val quranReelsDir = java.io.File(moviesDir, "Quran Reels/ERROR")
            if (!quranReelsDir.exists()) quranReelsDir.mkdirs()
            
            // Delete old error files
            quranReelsDir.listFiles()?.forEach { it.delete() }
            
            val file = java.io.File(quranReelsDir, fileName)
            java.io.PrintWriter(java.io.FileWriter(file)).use { it.print(reportContent) }
            finalPath = file.absolutePath
            com.example.utils.AppLogger.i("SystemDiagnosticTracker", "Report saved via public directory: $finalPath")
            return finalPath
        } catch (e: Exception) {
            com.example.utils.AppLogger.e("SystemDiagnosticTracker", "Failed to save via public directory", e)
        }"""

if old_tracker in content:
    content = content.replace(old_tracker, new_tracker)
    with open('app/src/main/java/com/example/generator/SystemDiagnosticTracker.kt', 'w') as f:
        f.write(content)
    print("Patched SystemDiagnosticTracker successfully")
else:
    print("Could not find old_tracker in SystemDiagnosticTracker")

