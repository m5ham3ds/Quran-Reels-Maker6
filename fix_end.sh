sed -i '650,670c\
                            Spacer(Modifier.width(6.dp))\
                            Text(if (isArabic) "توليد بالذكاء الاصطناعي" else "AI Auto Fill")\
                        }\
                    }\
                }\
            }\
\
            // Section 2: API Keys and Video Backdrop config\
            Text(\
                text = if (isArabic) "مصادر ومفاتيح الـ API" else "Integration & API Configuration",' app/src/main/java/com/example/ui/settings/SettingsScreen.kt
