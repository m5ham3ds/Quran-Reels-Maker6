import re
with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target = """                }.then(
                    if (showTextBackground) {
                        Modifier
                            .background(
                                color = tBgColor.copy(alpha = textBgOpacity),
                                shape = RoundedCornerShape(textBgRadius.dp)
                            )
                            .padding(horizontal = 20.dp, vertical = 24.dp)
                    } else {
                        Modifier
                    }
                ),"""

replacement = """                }.fillMaxWidth(0.9f).drawBehind {
                    if (showTextBackground) {
                        val finalBgColor = tBgColor.copy(alpha = textBgOpacity)
                        val padTop = 42f * canvasScale
                        val padBottom = 42f * canvasScale
                        drawRoundRect(
                            color = finalBgColor,
                            topLeft = androidx.compose.ui.geometry.Offset(0f, -padTop),
                            size = androidx.compose.ui.geometry.Size(size.width, size.height + padTop + padBottom),
                            cornerRadius = androidx.compose.ui.geometry.CornerRadius(textBgRadius.dp.toPx())
                        )
                    }
                },"""

if target in content:
    content = content.replace(target, replacement)
    print("Found and replaced!")
else:
    print("Not found.")

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)
