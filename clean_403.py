with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

bad_block = """                                                if (response.code == 403) {
                                                    withContext(Dispatchers.Main) {
                                                        android.widget.Toast.makeText(context, if (isArabic) "مفتاح API محظور أو تم تسريبه (خطأ 403). يرجى إنشاء مفتاح جديد." else "API key blocked or leaked (403). Please get a new one.", android.widget.Toast.LENGTH_LONG).show()
                                                    }
                                                }
                                                if (response.code == 403) {
                                                    withContext(Dispatchers.Main) {
                                                        android.widget.Toast.makeText(context, if (isArabic) "مفتاح API محظور أو تم تسريبه (خطأ 403). يرجى تغييره من Google AI Studio." else "API key blocked or leaked (403). Please get a new one.", android.widget.Toast.LENGTH_LONG).show()
                                                    }
                                                }"""

good_block = """                                                if (response.code == 403) {
                                                    withContext(Dispatchers.Main) {
                                                        android.widget.Toast.makeText(context, if (isArabic) "مفتاح API محظور أو تم تسريبه (خطأ 403). يرجى إنشاء مفتاح جديد." else "API key blocked or leaked (403). Please get a new one.", android.widget.Toast.LENGTH_LONG).show()
                                                    }
                                                }"""

if bad_block in content:
    content = content.replace(bad_block, good_block)
    print("Replaced bad block")

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)

