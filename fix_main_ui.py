import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    m = f.read()

m = m.replace(
    "val textAnimation by settingsManager.textAnimation.collectAsState(initial = \"Fade\")",
    "val textAnimation by settingsManager.textAnimation.collectAsState(initial = \"Fade\")\n    val textAnimationEnabled by settingsManager.textAnimationEnabled.collectAsState(initial = true)"
)

target_ui = """                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 10.dp)) {
                        Icon(Icons.Default.PlayArrow, contentDescription = null, tint = LuxuryGold, modifier = Modifier.size(22.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (isArabic) "حركة دخول الجمل" else "Text Entrance Animation", color = TextSoftColor, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    }

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        val animations = listOf("Fade" to (if(isArabic) "تلاشي" else "Fade"), "SlideUp" to (if(isArabic) "انزلاق" else "Slide Up"), "Scale" to (if(isArabic) "تكبير" else "Scale"), "None" to (if(isArabic) "بدون" else "None"))
                        animations.forEach { (anim, label) ->"""

replacement_ui = """                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween,
                        modifier = Modifier.fillMaxWidth().padding(top = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null, tint = LuxuryGold, modifier = Modifier.size(22.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(if (isArabic) "حركة دخول الجمل" else "Text Entrance Animation", color = TextSoftColor, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        }
                        Switch(
                            checked = textAnimationEnabled,
                            onCheckedChange = { scope.launch { settingsManager.setTextAnimationEnabled(it) } },
                            colors = SwitchDefaults.colors(
                                checkedThumbColor = ScreenBg,
                                checkedTrackColor = LuxuryGold,
                                uncheckedThumbColor = TextMutedColor,
                                uncheckedTrackColor = BorderColor
                            )
                        )
                    }

                    if (textAnimationEnabled) {
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            val animations = listOf("Fade" to (if(isArabic) "تلاشي" else "Fade"), "SlideUp" to (if(isArabic) "انزلاق لأعلى" else "Slide Up"), "SlideRight" to (if(isArabic) "انزلاق لليمين" else "Slide Right"), "Scale" to (if(isArabic) "تكبير" else "Scale"))
                            animations.forEach { (anim, label) ->"""

if target_ui in m:
    m = m.replace(target_ui, replacement_ui)
    
    # Also need to close the 'if (textAnimationEnabled) {' block at the end
    # Let's find the end of the animations forEach loop
    # It looks like:
    end_target = """                                        color = if (isSelected) ScreenBg else TextSoftColor,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 13.sp
                                    )
                                }
                            }
                        }
                    }"""
    end_replace = """                                        color = if (isSelected) ScreenBg else TextSoftColor,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 13.sp
                                    )
                                }
                            }
                        }
                    }
                    }"""
    m = m.replace(end_target, end_replace)
    print("UI replaced")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(m)
