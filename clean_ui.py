import re

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# I added these duplicate lines inside LaunchedEffect(Unit):
duplicate_block = """                                fontSize = settingsManager.fontSize.first().toFloat()
                                translationFontSize = settingsManager.translationFontSize.first().toFloat()
                                surahNameFontSize = settingsManager.surahNameFontSize.first().toFloat()
                                iconSize = settingsManager.iconSize.first().toFloat()
                                
                                textOpacity = settingsManager.textOpacity.first()
                                translationOpacity = settingsManager.translationOpacity.first()
                                surahNameOpacity = settingsManager.surahNameOpacity.first()
                                iconOpacity = settingsManager.iconOpacity.first()"""

content = content.replace(duplicate_block, "")

with open('app/src/main/java/com/example/ui/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
