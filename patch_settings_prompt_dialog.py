import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

# 1. Add backgroundKeywordsPrompt to the states
target_state = 'val backgroundKeywords by settingsManager.backgroundKeywords.collectAsState(initial = emptySet())'
replacement_state = '''val backgroundKeywords by settingsManager.backgroundKeywords.collectAsState(initial = emptySet())
    val backgroundKeywordsPrompt by settingsManager.backgroundKeywordsPrompt.collectAsState(initial = "")
    var showPromptDialog by remember { mutableStateOf(false) }'''
content = content.replace(target_state, replacement_state)

# 2. Add an Edit icon button next to "كلمات البحث للخلفيات" (Background Search Keywords)
target_header = '''            Text(
                text = if (isArabic) "كلمات البحث للخلفيات" else "Background Search Keywords",'''
replacement_header = '''            Row(
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
            }'''
content = content.replace(target_header, replacement_header)

# 3. Add the Dialog at the end of the content
target_dialog = '            // Section 2: API Keys and Video Backdrop config'
replacement_dialog = '''            if (showPromptDialog) {
                var editablePrompt by remember { mutableStateOf(backgroundKeywordsPrompt) }
                
                LaunchedEffect(backgroundKeywordsPrompt) {
                    if (editablePrompt.isEmpty()) {
                        editablePrompt = backgroundKeywordsPrompt
                    }
                }
                
                BasicAlertDialog(
                    onDismissRequest = { showPromptDialog = false },
                    modifier = Modifier.fillMaxWidth().padding(16.dp)
                ) {
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = com.example.CardBg,
                        border = BorderStroke(1.dp, Color(0x33FFFFFF))
                    ) {
                        Column(
                            modifier = Modifier.padding(20.dp),
                            verticalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            Text(
                                text = if (isArabic) "تعديل برومبت الكلمات البحثية" else "Edit Background Keywords Prompt",
                                color = com.example.LuxuryGold,
                                fontWeight = FontWeight.Bold,
                                fontSize = 18.sp
                            )
                            Text(
                                text = if (isArabic) "يمكنك تعديل الرسالة التي يتم إرسالها إلى نموذج الذكاء الاصطناعي لإنشاء كلمات البحث." else "You can modify the prompt sent to the AI model to generate search keywords.",
                                color = com.example.TextMutedColor,
                                fontSize = 13.sp
                            )
                            OutlinedTextField(
                                value = editablePrompt,
                                onValueChange = { editablePrompt = it },
                                modifier = Modifier.fillMaxWidth().height(200.dp),
                                textStyle = androidx.compose.ui.text.TextStyle(fontSize = 14.sp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White,
                                    focusedBorderColor = com.example.LuxuryGold,
                                    unfocusedBorderColor = Color(0x33FFFFFF),
                                    focusedContainerColor = Color(0x0FFFFFFF),
                                    unfocusedContainerColor = Color(0x05FFFFFF)
                                )
                            )
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.End,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                TextButton(onClick = { showPromptDialog = false }) {
                                    Text(if (isArabic) "إلغاء" else "Cancel", color = Color(0xFFEF5350))
                                }
                                Spacer(modifier = Modifier.width(8.dp))
                                Button(
                                    onClick = {
                                        scope.launch {
                                            settingsManager.saveBackgroundKeywordsPrompt(editablePrompt)
                                            showPromptDialog = false
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = com.example.LuxuryGold)
                                ) {
                                    Text(if (isArabic) "حفظ" else "Save", color = Color.Black)
                                }
                            }
                        }
                    }
                }
            }
            
            // Section 2: API Keys and Video Backdrop config'''
content = content.replace(target_dialog, replacement_dialog)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
