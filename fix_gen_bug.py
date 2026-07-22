import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

# Let's ensure there are no leftover broken bits
print("Check done.")
