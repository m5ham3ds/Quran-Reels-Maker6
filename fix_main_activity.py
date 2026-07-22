import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        }
    }
}
    } // Close outer box for LivePreview

@Composable"""

replacement = """        }
    }
    } // Close outer box for LivePreview
}

@Composable"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
