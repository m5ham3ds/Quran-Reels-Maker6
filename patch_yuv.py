import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

old_yuv = """    private fun convertYUVImageToBitmap(image: Image): Bitmap {
        val w = image.width
        val h = image.height
        val yPlane = image.planes[0]
        val uPlane = image.planes[1]
        val vPlane = image.planes[2]
        
        val yBuffer = yPlane.buffer
        val uBuffer = uPlane.buffer
        val vBuffer = vPlane.buffer
        
        val yRowStride = yPlane.rowStride
        val uRowStride = uPlane.rowStride
        val vRowStride = vPlane.rowStride
        val uPixelStride = uPlane.pixelStride
        val vPixelStride = vPlane.pixelStride
        
        if (reusableBitmap == null || reusableBitmap!!.width != w || reusableBitmap!!.height != h) {
            reusableBitmap?.recycle()
            reusableBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
        }
        if (reusablePixels == null || reusablePixels!!.size != w * h) {
            reusablePixels = IntArray(w * h)
        }
        val bitmap = reusableBitmap!!
        val pixels = reusablePixels!!
        
        var index = 0
        for (y in 0 until h) {
            val yRowStart = y * yRowStride
            for (x in 0 until w) {
                val yValue = (yBuffer.get(yRowStart + x).toInt() and 0xff)
                
                val uvIndex = (y / 2) * uRowStride + (x / 2) * uPixelStride
                val vIndex = (y / 2) * vRowStride + (x / 2) * vPixelStride
                
                val uValue = if (uvIndex < uBuffer.capacity()) (uBuffer.get(uvIndex).toInt() and 0xff) - 128 else 0
                val vValue = if (vIndex < vBuffer.capacity()) (vBuffer.get(vIndex).toInt() and 0xff) - 128 else 0
                
                var rCol = (yValue + 1.370705f * vValue).toInt()
                var gCol = (yValue - 0.337633f * uValue - 0.698001f * vValue).toInt()
                var bCol = (yValue + 1.732446f * uValue).toInt()
                
                rCol = rCol.coerceIn(0, 255)
                gCol = gCol.coerceIn(0, 255)
                bCol = bCol.coerceIn(0, 255)
                
                pixels[index++] = (0xff shl 24) or (rCol shl 16) or (gCol shl 8) or bCol
            }
        }
        bitmap.setPixels(pixels, 0, w, 0, 0, w, h)
        return bitmap
    }"""

new_yuv = """    private fun convertYUVImageToBitmap(image: Image): Bitmap {
        val w = image.width
        val h = image.height
        val yPlane = image.planes[0]
        val uPlane = image.planes[1]
        val vPlane = image.planes[2]
        
        val yBuffer = yPlane.buffer
        val uBuffer = uPlane.buffer
        val vBuffer = vPlane.buffer
        
        val yRowStride = yPlane.rowStride
        val uRowStride = uPlane.rowStride
        val vRowStride = vPlane.rowStride
        val uPixelStride = uPlane.pixelStride
        val vPixelStride = vPlane.pixelStride
        
        val maxDim = 1280
        val scale = Math.max(1, Math.max(w / maxDim, h / maxDim))
        
        val outW = w / scale
        val outH = h / scale
        
        if (reusableBitmap == null || reusableBitmap!!.width != outW || reusableBitmap!!.height != outH) {
            reusableBitmap?.recycle()
            reusableBitmap = Bitmap.createBitmap(outW, outH, Bitmap.Config.ARGB_8888)
        }
        if (reusablePixels == null || reusablePixels!!.size != outW * outH) {
            reusablePixels = IntArray(outW * outH)
        }
        val bitmap = reusableBitmap!!
        val pixels = reusablePixels!!
        
        var index = 0
        for (outY in 0 until outH) {
            val y = outY * scale
            val yRowStart = y * yRowStride
            for (outX in 0 until outW) {
                val x = outX * scale
                val yValue = (yBuffer.get(yRowStart + x).toInt() and 0xff)
                
                val uvIndex = (y / 2) * uRowStride + (x / 2) * uPixelStride
                val vIndex = (y / 2) * vRowStride + (x / 2) * vPixelStride
                
                val uValue = if (uvIndex < uBuffer.capacity()) (uBuffer.get(uvIndex).toInt() and 0xff) - 128 else 0
                val vValue = if (vIndex < vBuffer.capacity()) (vBuffer.get(vIndex).toInt() and 0xff) - 128 else 0
                
                var rCol = (yValue + 1.370705f * vValue).toInt()
                var gCol = (yValue - 0.337633f * uValue - 0.698001f * vValue).toInt()
                var bCol = (yValue + 1.732446f * uValue).toInt()
                
                rCol = if (rCol < 0) 0 else if (rCol > 255) 255 else rCol
                gCol = if (gCol < 0) 0 else if (gCol > 255) 255 else gCol
                bCol = if (bCol < 0) 0 else if (bCol > 255) 255 else bCol
                
                pixels[index++] = (0xff shl 24) or (rCol shl 16) or (gCol shl 8) or bCol
            }
        }
        bitmap.setPixels(pixels, 0, outW, 0, 0, outW, outH)
        return bitmap
    }"""

if old_yuv in content:
    content = content.replace(old_yuv, new_yuv)
    with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
        f.write(content)
    print("Patched convertYUVImageToBitmap successfully")
else:
    print("Could not find old_yuv in file")

