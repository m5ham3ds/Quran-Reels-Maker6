import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Fix Surah Name
target_surah = """        // Surah Name (Top)
        val sColor = try { Color(android.graphics.Color.parseColor(surahNameColorStr)) } catch (e: Exception) { Color.White }
        Text(
            text = "سُورَةُ الْكَوْثَرِ",
            fontFamily = finalSurahFontFamily,
            fontSize = (surahNameFontSize * scale / fontScale).sp,
            color = sColor.copy(alpha = surahNameOpacity),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 20.dp)
                .offset(x = (surahNameX * scale).dp, y = ((surahNameY + 40f) * scale).dp)
        )"""

replacement_surah = """        // Surah Name (Top)
        val sColor = try { Color(android.graphics.Color.parseColor(surahNameColorStr)) } catch (e: Exception) { Color.White }
        Text(
            text = "سُورَةُ الْكَوْثَرِ",
            fontFamily = finalSurahFontFamily,
            fontSize = (surahNameFontSize * scale / fontScale).sp,
            color = sColor.copy(alpha = surahNameOpacity),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .offset(x = (surahNameX * scale).dp, y = ((surahNameY + 180f) * scale).dp)
        )"""
content = content.replace(target_surah, replacement_surah)

# 2. Fix Icon
target_icon = """        // Qibla Icon
        Icon(
            imageVector = Icons.Outlined.FavoriteBorder,
            contentDescription = null,
            tint = Color.White.copy(alpha = iconOpacity),
            modifier = Modifier
                .align(Alignment.Center)
                .size((iconSize * scale).dp)
                .offset(x = (iconX * scale).dp, y = ((iconY + 45f) * scale).dp)
        )"""

replacement_icon = """        // Qibla Icon
        Icon(
            imageVector = Icons.Outlined.FavoriteBorder,
            contentDescription = null,
            tint = Color.White.copy(alpha = iconOpacity),
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .size((iconSize * scale).dp)
                .offset(x = (iconX * scale).dp, y = ((iconY - 200f) * scale).dp)
        )"""
content = content.replace(target_icon, replacement_icon)

# 3. Fix Text Block
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
                    verticalArrangement = Arrangement.spacedBy((32f * scale).dp),
                    modifier = Modifier
                        .fillMaxWidth(0.9f)
                        .drawBehind {
                            if (showTextBg) {
                                val padTop = 30f * scale * density
                                val padBottom = 30f * scale * density
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

# 4. Remove outer box padding
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

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
