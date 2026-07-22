import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

slider_code = """
                    } else if (selectedElement == "surah_name") {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(if (isArabic) "الحجم" else "Size", color = Color.White, fontSize = 12.sp)
                            Slider(
                                value = surahNameFontSize,
                                onValueChange = { surahNameFontSize = it },
                                valueRange = 10f..150f,
                                modifier = Modifier.width(120.dp),
                                colors = SliderDefaults.colors(thumbColor = LuxuryGold, activeTrackColor = LuxuryGold)
                            )
                        }
"""

content = content.replace('} else if (selectedElement == "translation") {', slider_code + '                    } else if (selectedElement == "translation") {')

# Also wait! Is selectedElement == "surah_name" possible?
# Let's check draggable boxes.

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)

