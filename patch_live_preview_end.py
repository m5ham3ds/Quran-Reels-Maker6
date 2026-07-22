import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

# The end of LivePreviewContainer is right before `@Composable fun GeneratedMetaSection`
# Let's find `@Composable\nfun GeneratedMetaSection`

for i, line in enumerate(lines):
    if "fun GeneratedMetaSection(" in line:
        # We need to insert `    }` before the `}` that closes LivePreviewContainer.
        # Lines:
        # 2793:         }
        # 2794:     }
        # 2795: }
        # 2796: 
        # 2797: @Composable
        
        # We can just insert it at i - 3
        lines.insert(i - 2, "    } // Close outer box for LivePreview\n")
        break

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(lines)

