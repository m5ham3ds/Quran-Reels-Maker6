import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Add states
content = content.replace(
    'val geminiModel by settingsManager.geminiModel.collectAsState(initial = "gemini-3.5-flash")',
    '''val geminiModel by settingsManager.geminiModel.collectAsState(initial = "gemini-3.5-flash")
    val aiPlatform by settingsManager.aiPlatform.collectAsState(initial = "Gemini")
    val huggingfaceKey by settingsManager.huggingfaceApiKey.collectAsState(initial = "")
    val huggingfaceModel by settingsManager.huggingfaceModel.collectAsState(initial = "Qwen/Qwen2.5-72B-Instruct")'''
)

# Add AI Platform Switcher in Appearance
theme_row = '''                            Switch(
                                checked = isDark,
                                onCheckedChange = { scope.launch { settingsManager.setThemeMode(it) } },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = LuxuryGold,
                                    checkedTrackColor = LuxuryGold.copy(alpha=0.4f)
                                )
                            )
                        }
                        HorizontalDivider(color = Color(0x15FFFFFF))'''

ai_switch = '''
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = LuxuryGold.copy(alpha=0.2f),
                                modifier = Modifier.size(40.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Default.SmartToy,
                                        contentDescription = null,
                                        tint = LuxuryGold
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = if (isArabic) "تحديد المنصة المستخدمة" else "AI Platform",
                                    color = Color.White,
                                    fontWeight = FontWeight.SemiBold,
                                    fontSize = 15.sp
                                )
                                Text(
                                    text = if (aiPlatform == "Gemini") (if (isArabic) "Gimien <== huggingface" else "Gemini <== huggingface") else (if (isArabic) "Gimien ==> huggingface" else "Gemini ==> huggingface"),
                                    color = TextMutedColor,
                                    fontSize = 12.sp,
                                    modifier = Modifier.padding(top = 2.dp)
                                )
                            }
                            Switch(
                                checked = aiPlatform == "HuggingFace",
                                onCheckedChange = { 
                                    scope.launch { 
                                        settingsManager.saveAiPlatform(if (it) "HuggingFace" else "Gemini") 
                                    } 
                                },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = LuxuryGold,
                                    checkedTrackColor = LuxuryGold.copy(alpha=0.4f)
                                )
                            )
                        }
                        HorizontalDivider(color = Color(0x15FFFFFF))
'''
content = content.replace(theme_row, theme_row + ai_switch)


# Replace AI fields
ai_section_start = '''                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(imageVector = Icons.Default.Key, contentDescription = null, tint = Color(0xBCFFFFFF), modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("Gemini AI Key", color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                                }'''

ai_section_full_old = '''                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(imageVector = Icons.Default.Key, contentDescription = null, tint = Color(0xBCFFFFFF), modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Text("Gemini AI Key", color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                                }
                                Text(
                                    text = if (isArabic) "احصل على مفتاح Gemini مجاناً" else "Get free Gemini key",
                                    color = LuxuryGold,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 12.sp,
                                    modifier = Modifier
                                        .clickable { uriHandler.openUri("https://aistudio.google.com/") }
                                        .padding(4.dp)
                                )
                            }
                            Text(
                                text = if (isArabic) "مطلوب لتوليد العناوين والوصف والهاشتاجات الذكية لكل منصة بشكل احترافي" else "Required to generate smart platform-specific titles, descriptions, and tags automatically",
                                color = TextMutedColor,
                                fontSize = 11.sp,
                                lineHeight = 15.sp,
                                modifier = Modifier.padding(bottom = 2.dp)
                            )
                            OutlinedTextField(
                                value = geminiKey,
                                onValueChange = { scope.launch { settingsManager.saveGeminiKey(it) } },
                                placeholder = { Text(if (isArabic) "أدخل مفتاح Gemini هنا لروبوت الذكاء الاصطناعي..." else "Paste your Gemini API key...", color = Color(0x61FFFFFF)) },
                                singleLine = true,
                                shape = RoundedCornerShape(12.dp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = LuxuryGold,
                                    unfocusedBorderColor = Color(0x33FFFFFF),
                                    focusedContainerColor = Color(0x0FFFFFFF),
                                    unfocusedContainerColor = Color(0x05FFFFFF)
                                ),
                                modifier = Modifier.fillMaxWidth()
                            )
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            Text(
                                text = if (isArabic) "نموذج الذكاء الاصطناعي (Gemini Model)" else "Gemini AI Model",
                                color = Color.White,
                                fontSize = 14.sp,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.padding(bottom = 6.dp)
                            )
                            val models = listOf(
                                "gemini-3.5-flash",
                                "gemini-3.1-pro-preview",
                                "gemini-3.1-flash-lite",
                                "gemini-2.5-flash"
                            )
                            FlowRow(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                models.forEach { model ->
                                    FilterChip(
                                        selected = geminiModel == model,
                                        onClick = { scope.launch { settingsManager.saveGeminiModel(model) } },
                                        label = { Text(model, color = if (geminiModel == model) Color.Black else Color.White) },
                                        colors = FilterChipDefaults.filterChipColors(
                                            selectedContainerColor = LuxuryGold,
                                            containerColor = Color(0x33FFFFFF)
                                        )
                                    )
                                }
                            }'''

ai_section_new = '''                            if (aiPlatform == "Gemini") {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(imageVector = Icons.Default.Key, contentDescription = null, tint = Color(0xBCFFFFFF), modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("Gemini AI Key", color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                                    }
                                    Text(
                                        text = if (isArabic) "احصل على مفتاح مجاناً" else "Get free key",
                                        color = LuxuryGold,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 12.sp,
                                        modifier = Modifier
                                            .clickable { uriHandler.openUri("https://aistudio.google.com/") }
                                            .padding(4.dp)
                                    )
                                }
                                Text(
                                    text = if (isArabic) "مطلوب لتوليد العناوين والوصف والهاشتاجات الذكية لكل منصة بشكل احترافي" else "Required to generate smart platform-specific titles, descriptions, and tags automatically",
                                    color = TextMutedColor,
                                    fontSize = 11.sp,
                                    lineHeight = 15.sp,
                                    modifier = Modifier.padding(bottom = 2.dp)
                                )
                                OutlinedTextField(
                                    value = geminiKey,
                                    onValueChange = { scope.launch { settingsManager.saveGeminiKey(it) } },
                                    placeholder = { Text(if (isArabic) "أدخل مفتاح Gemini هنا..." else "Paste your Gemini API key...", color = Color(0x61FFFFFF)) },
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        focusedTextColor = Color.White,
                                        unfocusedTextColor = Color.White,
                                        focusedBorderColor = LuxuryGold,
                                        unfocusedBorderColor = Color(0x33FFFFFF),
                                        focusedContainerColor = Color(0x0FFFFFFF),
                                        unfocusedContainerColor = Color(0x05FFFFFF)
                                    ),
                                    modifier = Modifier.fillMaxWidth()
                                )
                                
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = if (isArabic) "نموذج الذكاء الاصطناعي (Gemini Model)" else "Gemini AI Model",
                                    color = Color.White,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(bottom = 6.dp)
                                )
                                val models = listOf(
                                    "gemini-3.5-flash",
                                    "gemini-3.1-pro-preview",
                                    "gemini-3.1-flash-lite",
                                    "gemini-2.5-flash"
                                )
                                FlowRow(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    models.forEach { model ->
                                        FilterChip(
                                            selected = geminiModel == model,
                                            onClick = { scope.launch { settingsManager.saveGeminiModel(model) } },
                                            label = { Text(model, color = if (geminiModel == model) Color.Black else Color.White) },
                                            colors = FilterChipDefaults.filterChipColors(
                                                selectedContainerColor = LuxuryGold,
                                                containerColor = Color(0x33FFFFFF)
                                            )
                                        )
                                    }
                                }
                            } else {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(imageVector = Icons.Default.Key, contentDescription = null, tint = Color(0xBCFFFFFF), modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Text("Hugging Face API Key", color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                                    }
                                    Text(
                                        text = if (isArabic) "احصل على مفتاح مجاناً" else "Get free key",
                                        color = LuxuryGold,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 12.sp,
                                        modifier = Modifier
                                            .clickable { uriHandler.openUri("https://huggingface.co/settings/tokens") }
                                            .padding(4.dp)
                                    )
                                }
                                Text(
                                    text = if (isArabic) "بديل Gimien (Gemini) لاستخدام نماذج DeepSeek و Qwen" else "Gemini alternative to use DeepSeek and Qwen models",
                                    color = TextMutedColor,
                                    fontSize = 11.sp,
                                    lineHeight = 15.sp,
                                    modifier = Modifier.padding(bottom = 2.dp)
                                )
                                OutlinedTextField(
                                    value = huggingfaceKey,
                                    onValueChange = { scope.launch { settingsManager.saveHuggingfaceApiKey(it) } },
                                    placeholder = { Text(if (isArabic) "أدخل مفتاح Hugging Face هنا..." else "Paste your Hugging Face API key...", color = Color(0x61FFFFFF)) },
                                    singleLine = true,
                                    shape = RoundedCornerShape(12.dp),
                                    colors = OutlinedTextFieldDefaults.colors(
                                        focusedTextColor = Color.White,
                                        unfocusedTextColor = Color.White,
                                        focusedBorderColor = LuxuryGold,
                                        unfocusedBorderColor = Color(0x33FFFFFF),
                                        focusedContainerColor = Color(0x0FFFFFFF),
                                        unfocusedContainerColor = Color(0x05FFFFFF)
                                    ),
                                    modifier = Modifier.fillMaxWidth()
                                )
                                
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = if (isArabic) "نموذج الذكاء الاصطناعي (Hugging Face Model)" else "Hugging Face AI Model",
                                    color = Color.White,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(bottom = 6.dp)
                                )
                                val hfModels = listOf(
                                    "Qwen/Qwen2.5-72B-Instruct",
                                    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                                    "google/gemma-2-27b-it"
                                )
                                FlowRow(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    hfModels.forEach { model ->
                                        FilterChip(
                                            selected = huggingfaceModel == model,
                                            onClick = { scope.launch { settingsManager.saveHuggingfaceModel(model) } },
                                            label = { Text(model.split("/").last(), color = if (huggingfaceModel == model) Color.Black else Color.White) },
                                            colors = FilterChipDefaults.filterChipColors(
                                                selectedContainerColor = LuxuryGold,
                                                containerColor = Color(0x33FFFFFF)
                                            )
                                        )
                                    }
                                }
                            }'''

content = content.replace(ai_section_full_old, ai_section_new)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
