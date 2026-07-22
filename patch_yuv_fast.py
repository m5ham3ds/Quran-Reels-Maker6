import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

# We need to replace the floating point math in convertYUVImageToBitmap
old_math = """                var rCol = (yValue + 1.370705f * vValue).toInt()
                var gCol = (yValue - 0.337633f * uValue - 0.698001f * vValue).toInt()
                var bCol = (yValue + 1.732446f * uValue).toInt()"""

new_math = """                var rCol = yValue + ((vValue * 1436) shr 10)
                var gCol = yValue - ((uValue * 352 + vValue * 731) shr 10)
                var bCol = yValue + ((uValue * 1814) shr 10)"""

if old_math in content:
    content = content.replace(old_math, new_math)
    with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
        f.write(content)
    print("Patched math successfully")
else:
    print("Could not find old_math in file")

