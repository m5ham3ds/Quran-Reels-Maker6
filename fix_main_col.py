import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = (if (showTextBg) {
                        val bgColor = try { Color(android.graphics.Color.parseColor(textBgColorStr)) } catch (e: Exception) { Color.Black }
                        Modifier
                            .background(
                                color = bgColor.copy(alpha = textBgOpacity),
                                shape = RoundedCornerShape(textBgRadius.dp)
                            )
                            .padding(horizontal = 20.dp, vertical = 24.dp)
                    } else {
                        Modifier
                    }).then(if (textPosition == "Center" || textPosition == "Middle") Modifier.offset(y = (150f * scale).dp) else Modifier)
                ) {"""

replacement = """                    verticalArrangement = Arrangement.spacedBy((32f * scale).dp),
                    modifier = Modifier.fillMaxWidth(0.9f).drawBehind {
                        if (showTextBg) {
                            val bgColor = try { Color(android.graphics.Color.parseColor(textBgColorStr)) } catch (e: Exception) { Color.Black }
                            val finalBgColor = bgColor.copy(alpha = textBgOpacity)
                            val padTop = 30f * scale * density
                            val padBottom = 30f * scale * density
                            drawRoundRect(
                                color = finalBgColor,
                                topLeft = androidx.compose.ui.geometry.Offset(0f, -padTop),
                                size = androidx.compose.ui.geometry.Size(size.width, size.height + padTop + padBottom),
                                cornerRadius = androidx.compose.ui.geometry.CornerRadius(textBgRadius.dp.toPx())
                            )
                        }
                    }.then(if (textPosition == "Center" || textPosition == "Middle") Modifier.offset(y = (150f * scale).dp) else Modifier)
                ) {"""

if target in content:
    content = content.replace(target, replacement)
    print("Main Column fixed!")
else:
    print("Main Column target not found.")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
