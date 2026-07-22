import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

target = '''                        HorizontalDivider(color = Color(0x15FFFFFF))

                        // Language picker Custom Dropdown'''

replacement = '''                        HorizontalDivider(color = Color(0x15FFFFFF))

                        // AI Platform Switcher
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text(
                                text = if (isArabic) "تحديد المنصة المستخدمة" else "Select AI Platform",
                                color = Color.White,
                                fontWeight = FontWeight.SemiBold,
                                fontSize = 15.sp
                            )
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp),
                                horizontalArrangement = Arrangement.Center,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "Gemini",
                                    color = if (aiPlatform == "Gemini") com.example.ui.theme.LuxuryGold else com.example.ui.theme.TextMutedColor,
                                    fontWeight = if (aiPlatform == "Gemini") FontWeight.Bold else FontWeight.Normal,
                                    fontSize = 16.sp,
                                    modifier = Modifier.clickable { scope.launch { settingsManager.saveAiPlatform("Gemini") } }
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Switch(
                                    checked = aiPlatform == "HuggingFace",
                                    onCheckedChange = { isHF -> 
                                        scope.launch { settingsManager.saveAiPlatform(if (isHF) "HuggingFace" else "Gemini") }
                                    },
                                    colors = SwitchDefaults.colors(
                                        checkedThumbColor = com.example.ui.theme.LuxuryGold,
                                        checkedTrackColor = com.example.ui.theme.LuxuryGold.copy(alpha=0.4f),
                                        uncheckedThumbColor = com.example.ui.theme.LuxuryGold,
                                        uncheckedTrackColor = com.example.ui.theme.LuxuryGold.copy(alpha=0.4f)
                                    ),
                                    thumbContent = {
                                        if (aiPlatform == "HuggingFace") {
                                            Icon(imageVector = androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, modifier = Modifier.size(12.dp))
                                        } else {
                                            Icon(imageVector = androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null, modifier = Modifier.size(12.dp))
                                        }
                                    }
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(
                                    text = "HuggingFace",
                                    color = if (aiPlatform == "HuggingFace") com.example.ui.theme.LuxuryGold else com.example.ui.theme.TextMutedColor,
                                    fontWeight = if (aiPlatform == "HuggingFace") FontWeight.Bold else FontWeight.Normal,
                                    fontSize = 16.sp,
                                    modifier = Modifier.clickable { scope.launch { settingsManager.saveAiPlatform("HuggingFace") } }
                                )
                            }
                        }

                        HorizontalDivider(color = Color(0x15FFFFFF))

                        // Language picker Custom Dropdown'''

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
