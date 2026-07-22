import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

social_overlay = """
        // Realistic Reel Social Overlay
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(18.dp),
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(end = 12.dp, bottom = 40.dp)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                IconButton(onClick = {}) {
                    Icon(Icons.Filled.Favorite, contentDescription = null, tint = Color(0xFFE91E63), modifier = Modifier.size(26.dp))
                }
                Text("1.2K", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
            
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                IconButton(onClick = {}) {
                    Icon(Icons.Filled.Home, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
                }
                Text("48", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
            
            IconButton(onClick = {}) {
                Icon(Icons.Filled.Send, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
            }
            
            // Spinning disk silhouette
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .border(2.dp, Color.White.copy(alpha = 0.5f), CircleShape)
                    .background(Color.Black, CircleShape)
            )
        }
"""

# Find where to insert it. Before "// Live Preview Eyes banner"
target = "// Live Preview Eyes banner"
if target in content:
    content = content.replace(target, social_overlay + "\n        " + target)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

