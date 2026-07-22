import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'put("text", "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. \'islamic aesthetics kaaba mecca\', \'dark cinematic aesthetic landscape\', \'stormy rain window\', \'stars night sky\'). Return ONLY a comma-separated list of strings.")',
    'put("text", backgroundKeywordsPrompt.ifBlank { "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. \'islamic aesthetics kaaba mecca\', \'dark cinematic aesthetic landscape\', \'stormy rain window\', \'stars night sky\'). Return ONLY a comma-separated list of strings." })'
)

if 'showKeywordPromptDialog = false' not in content:
    content = content.rstrip()
    if content.endswith('}'):
        content = content[:-1]
    
    content += """
    if (showKeywordPromptDialog) {
        var editablePrompt by remember { mutableStateOf(backgroundKeywordsPrompt.ifBlank { "Generate 10 English keywords or short phrases optimized for Pexels/Pixabay to find aesthetic cinematic, nature, atmospheric, and Islamic-themed background videos (e.g. 'islamic aesthetics kaaba mecca', 'dark cinematic aesthetic landscape', 'stormy rain window', 'stars night sky'). Return ONLY a comma-separated list of strings." }) }
        
        AlertDialog(
            onDismissRequest = { showKeywordPromptDialog = false },
            containerColor = CardBg,
            title = {
                Text(
                    text = if (isArabic) "تعديل برومبت الكلمات المرجعية" else "Edit Background Keywords Prompt",
                    color = LuxuryGold,
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                OutlinedTextField(
                    value = editablePrompt,
                    onValueChange = { editablePrompt = it },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = LuxuryGold,
                        unfocusedBorderColor = Color(0x33FFFFFF),
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    ),
                    modifier = Modifier.fillMaxWidth().height(200.dp),
                    textStyle = androidx.compose.ui.text.TextStyle(fontSize = 14.sp)
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        scope.launch { settingsManager.saveBackgroundKeywordsPrompt(editablePrompt) }
                        showKeywordPromptDialog = false
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = LuxuryGold)
                ) {
                    Text(if (isArabic) "حفظ" else "Save")
                }
            },
            dismissButton = {
                TextButton(onClick = { showKeywordPromptDialog = false }) {
                    Text(if (isArabic) "إلغاء" else "Cancel", color = TextSoftColor)
                }
            }
        )
    }
}
"""

content = content.replace(
    'val errorBody = response.body?.string() ?: ""',
    'val errorBody = response.body?.string() ?: ""\n                                                if (response.code == 403) {\n                                                    withContext(Dispatchers.Main) {\n                                                        android.widget.Toast.makeText(context, if (isArabic) "مفتاح API محظور أو تم تسريبه (خطأ 403). يرجى إنشاء مفتاح جديد." else "API key blocked or leaked (403). Please get a new one.", android.widget.Toast.LENGTH_LONG).show()\n                                                    }\n                                                }'
)

content = content.replace(
    '} else if (response.code == 429) {',
    '} else if (response.code == 429 || response.code == 503) {'
)
content = content.replace(
    'لقد استنفذت الحد المسموح (خطأ 429)',
    'لقد استنفذت الحد المسموح أو السيرفر مشغول (429/503)'
)
content = content.replace(
    'Rate limit reached (429)',
    'Rate limit or overloaded (429/503)'
)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)

