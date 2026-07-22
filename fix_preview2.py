import re

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "r") as f:
    v = f.read()

target = """                } else {
                    Text(
                        text = if (isArabic) "جاري التحميل..." else "Loading...",
                        color = Color.White,
                        modifier = Modifier.align(Alignment.Center)
                    )
                }"""

replacement = """                } else {
                    Text(
                        text = if (isArabic) "جاري التحميل..." else "Loading...",
                        color = Color.White,
                        modifier = Modifier.align(Alignment.Center)
                    )
                }

                // Background Transition Overlay for Live Preview
                if (bgTransitionEnabled && timelineChunks.isNotEmpty()) {
                    val activeChunkIndex = timelineChunks.indexOfFirst { currentTime >= it.startTimeMs && currentTime <= it.endTimeMs }
                    if (activeChunkIndex > 0) {
                        val activeChunk = timelineChunks[activeChunkIndex]
                        val prevChunk = timelineChunks[activeChunkIndex - 1]
                        if (activeChunk.bgIndex != prevChunk.bgIndex) {
                            val chunkTimeMs = currentTime - activeChunk.startTimeMs
                            if (chunkTimeMs < 500L) {
                                val progress = chunkTimeMs.toFloat() / 500f
                                when (bgTransitionType.lowercase()) {
                                    "black" -> {
                                        val alpha = if (progress < 0.5f) {
                                            (progress * 2f).coerceIn(0f, 1f)
                                        } else {
                                            (1f - (progress - 0.5f) * 2f).coerceIn(0f, 1f)
                                        }
                                        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = alpha)))
                                    }
                                    "blink" -> {
                                        if (progress < 0.15f) {
                                            Box(modifier = Modifier.fillMaxSize().background(Color.White))
                                        }
                                    }
                                    "dissolve" -> {
                                        // Approximate dissolve with a dip to black
                                        val alpha = if (progress < 0.5f) {
                                            (progress * 2f).coerceIn(0f, 1f) * 0.7f
                                        } else {
                                            (1f - (progress - 0.5f) * 2f).coerceIn(0f, 1f) * 0.7f
                                        }
                                        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = alpha)))
                                    }
                                    "vertical" -> {
                                        // A simple slide down of a black overlay to approximate vertical transition
                                        val alpha = 1f - progress
                                        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = alpha * 0.5f)))
                                    }
                                }
                            }
                        }
                    }
                }"""

if target in v:
    v = v.replace(target, replacement)
    print("Added transition overlay")
else:
    print("Could not find target for transition overlay")

with open("app/src/main/java/com/example/ui/VideoEditorScreen.kt", "w") as f:
    f.write(v)
