import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# I will replace the BoxWithConstraints block to use a safer sizing
# find the lines around 456
target = """
                    BoxWithConstraints(
                modifier = Modifier
                    .fillMaxHeight()
                    .aspectRatio(9f / 16f)
                    .background(Color.Black)
            ) {
"""

replacement = """
                    BoxWithConstraints(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(Color.Black),
                        contentAlignment = Alignment.Center
                    ) {
                        val actualWidthDp = minOf(maxWidth, maxHeight * (9f / 16f))
                        val actualHeightDp = actualWidthDp * (16f / 9f)
                        
                        Box(
                            modifier = Modifier
                                .size(actualWidthDp, actualHeightDp)
                                .background(Color.Black)
                        ) {
"""

content = content.replace(target, replacement)
# also add the closing brace for the new Box
# I see:
#             } // Close BoxWithConstraints
#             } // Close inner Box
#             } // Close LTR Provider
# So I need to replace:
#             } // Close BoxWithConstraints
# with
#             } } // Close Box and BoxWithConstraints

content = content.replace("            } // Close BoxWithConstraints", "            } } // Close Box and BoxWithConstraints")

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)

