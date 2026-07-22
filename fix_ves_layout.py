import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# 1. Fix Surah Name Handle
target_surah = """            // Surah Name Handle
            Box(
                modifier = Modifier
                    .offset { IntOffset((surahNameX * scalePx).roundToInt(), ((surahNameY + 40f) * scalePx).roundToInt()) }
                    .align(Alignment.TopCenter)
                    .padding(top = 90.dp)"""

replacement_surah = """            // Surah Name Handle
            Box(
                modifier = Modifier
                    .align(Alignment.TopCenter)
                    .offset { IntOffset((surahNameX * scalePx).roundToInt(), ((surahNameY + 180f) * scalePx).roundToInt()) }"""
content = content.replace(target_surah, replacement_surah)

# 2. Fix Icon Handle
target_icon = """            // Icon Handle
            if (iconOpacity > 0f || selectedElement == "icon") {
                Box(
                    modifier = Modifier
                        .offset { IntOffset((iconX * scalePx).roundToInt(), ((iconY + 45f) * scalePx).roundToInt()) }
                        .align(Alignment.Center)"""

replacement_icon = """            // Icon Handle
            if (iconOpacity > 0f || selectedElement == "icon") {
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .offset { IntOffset((iconX * scalePx).roundToInt(), ((iconY - 200f) * scalePx).roundToInt()) }"""
content = content.replace(target_icon, replacement_icon)

# 3. Fix Text Block Spacing
target_spacing = """                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier
                        .then(
                            if (showTextBg) Modifier
                                .background(
                                    finalBgColor,
                                    RoundedCornerShape(16.dp)
                                )
                                .padding(16.dp)
                            else Modifier
                        )
                ) {"""

replacement_spacing = """                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(dpFromCanvas(32f)),
                    modifier = Modifier
                        .fillMaxWidth(0.9f)
                        .drawBehind {
                            if (showTextBg) {
                                val padTop = 30f * canvasScale
                                val padBottom = 30f * canvasScale
                                drawRoundRect(
                                    color = finalBgColor,
                                    topLeft = androidx.compose.ui.geometry.Offset(0f, -padTop),
                                    size = androidx.compose.ui.geometry.Size(size.width, size.height + padTop + padBottom),
                                    cornerRadius = androidx.compose.ui.geometry.CornerRadius(16.dp.toPx())
                                )
                            }
                        }
                ) {"""
content = content.replace(target_spacing, replacement_spacing)

# 4. Remove outer box padding in Text Positioner Frame
target_outer = """        // Text Positioner Frame
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 24.dp, vertical = 50.dp),"""
replacement_outer = """        // Text Positioner Frame
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(vertical = 50.dp),"""
content = content.replace(target_outer, replacement_outer)


with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(content)
