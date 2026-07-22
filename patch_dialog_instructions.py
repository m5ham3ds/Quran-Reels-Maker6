import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

target = '''                            Text(
                                text = if (isArabic) "يمكنك تعديل الرسالة التي يتم إرسالها إلى نموذج الذكاء الاصطناعي لإنشاء كلمات البحث." else "You can modify the prompt sent to the AI model to generate search keywords.",
                                color = com.example.TextMutedColor,
                                fontSize = 13.sp
                            )'''

replacement = '''                            Text(
                                text = if (isArabic) "يمكنك تعديل الرسالة الموجهة للذكاء الاصطناعي.\nملاحظة هامة: يجب أن تطلب من النموذج إرجاع الكلمات مفصولة بفاصلة (,) فقط بدون أي نصوص إضافية." else "You can modify the prompt sent to the AI model.\nNote: You MUST instruct the model to return the keywords separated by commas (,) only, without any other text.",
                                color = com.example.TextMutedColor,
                                fontSize = 13.sp
                            )'''

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
