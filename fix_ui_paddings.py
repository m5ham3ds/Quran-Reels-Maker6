import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Replace offsets
content = content.replace("surahNameY - 70f", "surahNameY - 40f")
content = content.replace("arabicTextY - 70f", "arabicTextY - 160f")
content = content.replace("translationTextY - 110f", "translationTextY - 230f")
content = content.replace("iconY + 50f", "iconY + 120f")

# Remove paddings inside the boxes to match generator
# We can't just replace all `.padding(16.dp)` because some might be legitimate (like outer layout padding).
# Let's find and remove the specific ones.

# Arabic Box:
arabic_box = """.clickable { selectedElement = "arabic" }
                        .border(if (selectedElement == "arabic") 2.dp else 0.dp, if (selectedElement == "arabic") LuxuryGold else Color.Transparent, RoundedCornerShape(4.dp))
                        .padding(16.dp)"""
content = content.replace(arabic_box, arabic_box.replace(".padding(16.dp)", ""))

# Translation Box:
trans_box = """.clickable { selectedElement = "translation" }
                            .border(if (selectedElement == "translation") 2.dp else 0.dp, if (selectedElement == "translation") LuxuryGold else Color.Transparent, RoundedCornerShape(4.dp))
                            .padding(16.dp)"""
content = content.replace(trans_box, trans_box.replace(".padding(16.dp)", ""))

# Surah Box:
surah_box = """.clickable { selectedElement = "surah" }
                    .border(if (selectedElement == "surah") 2.dp else 0.dp, if (selectedElement == "surah") LuxuryGold else Color.Transparent, RoundedCornerShape(4.dp))
                    .padding(8.dp)"""
content = content.replace(surah_box, surah_box.replace(".padding(8.dp)", ""))

# Icon Box:
icon_box = """.clickable { selectedElement = "icon" }
                        .border(if (selectedElement == "icon") 2.dp else 0.dp, if (selectedElement == "icon") LuxuryGold else Color.Transparent, RoundedCornerShape(4.dp))
                        .padding(8.dp)"""
content = content.replace(icon_box, icon_box.replace(".padding(8.dp)", ""))

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
