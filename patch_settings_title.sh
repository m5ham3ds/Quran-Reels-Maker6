sed -i '429,437c\
            // Section 1.5: Background Search Keywords\
            Row(\
                modifier = Modifier.fillMaxWidth().padding(start = 4.dp, top = 8.dp, end = 4.dp),\
                horizontalArrangement = Arrangement.SpaceBetween,\
                verticalAlignment = Alignment.CenterVertically\
            ) {\
                Text(\
                    text = if (isArabic) "كلمات البحث للخلفيات" else "Background Search Keywords",\
                    color = LuxuryGold,\
                    fontWeight = FontWeight.Bold,\
                    fontSize = 15.sp,\
                    letterSpacing = 0.5.sp\
                )\
                IconButton(\
                    onClick = { showKeywordPromptDialog = true },\
                    modifier = Modifier.size(32.dp)\
                ) {\
                    Icon(Icons.Default.Edit, contentDescription = "Edit Prompt", tint = LuxuryGold)\
                }\
            }' app/src/main/java/com/example/ui/settings/SettingsScreen.kt
