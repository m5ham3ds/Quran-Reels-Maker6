import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(9f / 16f)
            .clip(RoundedCornerShape(24.dp))
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A14), Color(0xFF140D07))
                )
            )
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""

replacement = """    Box(
        modifier = Modifier.fillMaxWidth().height(520.dp),
        contentAlignment = Alignment.Center
    ) {
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
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""

content = content.replace(target, replacement)

# We also need to add a closing brace.
# Find the end of LivePreviewContainer
# LivePreviewContainer is a composable function
# I'll just append it before the end of the file or at the end of LivePreviewContainer.
# Actually, I can search for `        // Live Preview Eyes banner` and find its closing brace.
# LivePreviewContainer starts at 2480. Let's find the closing brace.
