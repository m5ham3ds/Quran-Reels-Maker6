import os

ma_path = "app/src/main/java/com/example/MainActivity.kt"
with open(ma_path, "r") as f:
    content = f.read()

# Add to LivePreviewContainer signature
sig_target = """    iconY: Int,
    textAnimation: String,
    isArabic: Boolean,"""
sig_replace = """    iconY: Int,
    textAnimation: String,
    bgTransitionEnabled: Boolean,
    bgTransitionType: String,
    isArabic: Boolean,"""
content = content.replace(sig_target, sig_replace)

# Pass it from FontFormattingScreen
call_target = """                iconY = iconY,
                textAnimation = textAnimation,
                isArabic = isArabic,
                triggerRecomposition = triggerRecomposition"""
call_replace = """                iconY = iconY,
                textAnimation = textAnimation,
                bgTransitionEnabled = bgTransitionEnabled,
                bgTransitionType = bgTransitionType,
                isArabic = isArabic,
                triggerRecomposition = triggerRecomposition"""
content = content.replace(call_target, call_replace)

# Add transition logic inside LivePreviewContainer
# Find the BoxWithConstraints part
box_target = """    BoxWithConstraints(
        modifier = Modifier
            .fillMaxHeight()
            .aspectRatio(9f / 16f)
            .clip(RoundedCornerShape(24.dp))
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A14), Color(0xFF140D07))
                )
            )
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""

box_replace = """    var lastSentenceChangeTime by remember { mutableStateOf(0L) }
    var currentSentenceIndex by remember { mutableStateOf(0) }
    if (sentenceIndex != currentSentenceIndex) {
        currentSentenceIndex = sentenceIndex
        lastSentenceChangeTime = System.currentTimeMillis()
    }
    
    val timeSinceChange = System.currentTimeMillis() - lastSentenceChangeTime
    var bgAlphaOverlay = 0f
    var bgWhiteOverlay = 0f
    
    if (bgTransitionEnabled && timeSinceChange < 500L && isPlaying) {
        val progress = timeSinceChange.toFloat() / 500f
        when (bgTransitionType.lowercase()) {
            "black" -> {
                bgAlphaOverlay = if (progress < 0.5f) {
                    (progress * 2f).coerceIn(0f, 1f)
                } else {
                    (1f - (progress - 0.5f) * 2f).coerceIn(0f, 1f)
                }
            }
            "blink" -> {
                if (progress < 0.15f) bgWhiteOverlay = 1f
            }
            "dissolve" -> {
                bgAlphaOverlay = if (progress < 0.5f) {
                    (progress * 2f).coerceIn(0f, 1f) * 0.7f
                } else {
                    (1f - (progress - 0.5f) * 2f).coerceIn(0f, 1f) * 0.7f
                }
            }
            "vertical" -> {
                bgAlphaOverlay = (1f - progress) * 0.5f
            }
        }
    }
    // trigger recomposition for animation
    LaunchedEffect(timeSinceChange, isPlaying) {
        if (isPlaying && timeSinceChange < 500L) {
            kotlinx.coroutines.delay(16)
            lastSentenceChangeTime = lastSentenceChangeTime // trigger recomposition
        }
    }

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxHeight()
            .aspectRatio(9f / 16f)
            .clip(RoundedCornerShape(24.dp))
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A14), Color(0xFF140D07))
                )
            )
            .drawBehind {
                if (bgAlphaOverlay > 0f) {
                    drawRect(Color.Black.copy(alpha = bgAlphaOverlay))
                }
                if (bgWhiteOverlay > 0f) {
                    drawRect(Color.White.copy(alpha = bgWhiteOverlay))
                }
            }
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""
content = content.replace(box_target, box_replace)

# Fix baselines in LivePreviewContainer
content = content.replace("arabicTextY - 160f", "arabicTextY")
content = content.replace("translationTextY - 225f", "translationTextY")

with open(ma_path, "w") as f:
    f.write(content)
