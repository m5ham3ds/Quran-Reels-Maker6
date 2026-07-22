import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Fix the broken syntax
bad_syntax = """            Row(
                modifier = Modifier.fillMaxWidth().padding(start = 4.dp, top = 8.dp, end = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = if (isArabic) "كلمات البحث للخلفيات" else "Background Search Keywords",
                    color = com.example.LuxuryGold,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    letterSpacing = 0.5.sp
                )
                IconButton(
                    onClick = { showPromptDialog = true },
                    modifier = Modifier.size(24.dp)
                ) {
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Default.Edit,
                        contentDescription = "Edit Prompt",
                        tint = com.example.LuxuryGold
                    )
                }
            }
                color = LuxuryGold,
                fontWeight = FontWeight.Bold,
                fontSize = 15.sp,
                letterSpacing = 0.5.sp,
                modifier = Modifier.padding(start = 4.dp, top = 8.dp)
            )"""

good_syntax = """            Row(
                modifier = Modifier.fillMaxWidth().padding(start = 4.dp, top = 8.dp, end = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = if (isArabic) "كلمات البحث للخلفيات" else "Background Search Keywords",
                    color = com.example.LuxuryGold,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    letterSpacing = 0.5.sp
                )
                IconButton(
                    onClick = { showPromptDialog = true },
                    modifier = Modifier.size(24.dp)
                ) {
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Default.Edit,
                        contentDescription = "Edit Prompt",
                        tint = com.example.LuxuryGold
                    )
                }
            }"""

if bad_syntax in content:
    content = content.replace(bad_syntax, good_syntax)
elif "color = LuxuryGold," in content[content.find("Background Search Keywords"):]:
    # manual regex fix if exactly matches
    content = re.sub(
        r'}\s*color = LuxuryGold,\s*fontWeight = FontWeight\.Bold,\s*fontSize = 15\.sp,\s*letterSpacing = 0\.5\.sp,\s*modifier = Modifier\.padding\(start = 4\.dp, top = 8\.dp\)\s*\)',
        '}',
        content
    )

# Fix the URL scope
url_fix_target = r'val errorBody = response\.body\?\.string\(\) \?\: ""\s*com\.example\.generator\.SystemDiagnosticTracker\.addLog\("ERROR", "فشل الاتصال: رمز الاستجابة \$\{response\.code\}، التفاصيل: \$errorBody\\nالرابط كان: \$url"\)'
url_fix_replacement = '''val errorBody = response.body?.string() ?: ""
                                                com.example.generator.SystemDiagnosticTracker.addLog("ERROR", "فشل الاتصال: رمز الاستجابة ${response.code}، التفاصيل: $errorBody")'''
content = re.sub(url_fix_target, url_fix_replacement, content)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
