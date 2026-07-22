import re

with open('app/src/main/java/com/example/generator/GeminiMetaGenerator.kt', 'r') as f:
    content = f.read()

target = '''        SystemDiagnosticTracker.addLog("GEMINI", "تم جلب المعلومات بنجاح وإعدادها. جاري الانتقال إلى إرسال المعلومات والبرومبت الاحترافي إلى نموذج ذكاء اصطناعي Gemini...")
        
        val prompt = """
            أنت خبير في التعرف على تلاوات القرآن الكريم.
            لدينا مقطع فيديو/صوت بهذا الرابط: $videoUrl
            والنص المستخرج منه (إن وجد): "$transcription"
            وبعض البيانات الوصفية من الفيديو (العنوان، الوصف، الكلمات المفتاحية):
            $videoInfo
            ملاحظة (إن وجدت مشكلة في جلب النص): $whisperError
            
            يرجى تحليل النص المستخرج (أو الاعتماد على الرابط والبيانات الوصفية) لاستخراج المعلومات التالية:
            1. رقم السورة (1 إلى 114).
            2. رقم آية البداية.
            3. رقم آية النهاية.
            4. اسم القارئ (مثل: مشاري العفاسي، عبدالباسط عبدالصمد... إذا لم تكن متأكدا اكتب "غير معروف"). ابحث جيداً في العنوان أو الوصف أو الكلمات المفتاحية.
            5. عنوان مناسب للمقطع (مثل: تلاوة خاشعة بصوت...).
            6. التصنيف الروحي (اختر واحدًا من: طمأنينة، خشوع، سكينة، دعاء).
            
            إذا لم تتمكن من تحديد السورة والآيات، افترض سورة الفاتحة (1) والآيات 1 إلى 5.
            
            يجب أن يكون الرد حصرياً بصيغة JSON بالتنسيق التالي بدون أي نصوص إضافية:
            {
                "surah": 1,
                "startAyah": 1,
                "endAyah": 5,
                "reciterName": "اسم القارئ",
                "title": "عنوان المقطع",
                "category": "خشوع"
            }
        """.trimIndent()'''

replacement = '''        SystemDiagnosticTracker.addLog("GEMINI", "تم جلب المعلومات بنجاح وإعدادها. جاري الانتقال إلى إرسال المعلومات والبرومبت الاحترافي إلى نموذج ذكاء اصطناعي...")
        
        val userPromptTemplate = settingsManager.geminiPrompt.first()
        val defaultTemplate = """
            أنت خبير في التعرف على تلاوات القرآن الكريم.
            لدينا مقطع فيديو/صوت بهذا الرابط: [URL]
            والنص المستخرج منه (إن وجد): "[WHISPER_TEXT]"
            وبعض البيانات الوصفية من الفيديو (العنوان، الوصف، الكلمات المفتاحية):
            $videoInfo
            ملاحظة (إن وجدت مشكلة في جلب النص): $whisperError
            
            يرجى تحليل النص المستخرج (أو الاعتماد على الرابط والبيانات الوصفية) لاستخراج المعلومات التالية:
            1. رقم السورة (1 إلى 114).
            2. رقم آية البداية.
            3. رقم آية النهاية.
            4. اسم القارئ (مثل: مشاري العفاسي، عبدالباسط عبدالصمد... إذا لم تكن متأكدا اكتب "غير معروف"). ابحث جيداً في العنوان أو الوصف أو الكلمات المفتاحية.
            5. عنوان مناسب للمقطع (مثل: تلاوة خاشعة بصوت...).
            6. التصنيف الروحي (اختر واحدًا من: طمأنينة، خشوع، سكينة، دعاء).
            
            إذا لم تتمكن من تحديد السورة والآيات، افترض سورة الفاتحة (1) والآيات 1 إلى 5.
            
            يجب أن يكون الرد حصرياً بصيغة JSON بالتنسيق التالي بدون أي نصوص إضافية:
            {
                "surah": 1,
                "startAyah": 1,
                "endAyah": 5,
                "reciterName": "اسم القارئ",
                "title": "عنوان المقطع",
                "category": "خشوع"
            }
        """.trimIndent()
        
        val finalTemplate = if (userPromptTemplate.isBlank()) defaultTemplate else userPromptTemplate
        
        val prompt = finalTemplate
            .replace("[URL]", videoUrl)
            .replace("[WHISPER_TEXT]", transcription)
            .replace("$videoInfo", videoInfo)
            .replace("$whisperError", whisperError)'''

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/generator/GeminiMetaGenerator.kt', 'w') as f:
    f.write(content)
