import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

old_check = "if (reusableBitmap == null || reusableBitmap!!.width != outW || reusableBitmap!!.height != outH) {"
new_check = "if (reusableBitmap == null || reusableBitmap!!.isRecycled || reusableBitmap!!.width != outW || reusableBitmap!!.height != outH) {"

if old_check in content:
    content = content.replace(old_check, new_check)
    with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
        f.write(content)
    print("Patched recycled check successfully")
else:
    print("Could not find old_check in file")

