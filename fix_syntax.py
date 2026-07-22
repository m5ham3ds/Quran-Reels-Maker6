import re

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'r') as f:
    content = f.read()

content = content.replace('''        } catch (e: Exception) {
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
        }
        }
        return@withContext null
    }''', '''        } catch (e: Exception) {
            com.example.utils.AppLogger.e("ExceptionCatch", "Exception caught: ${ e.message }", e)
        }
        return@withContext null
    }''')

with open('app/src/main/java/com/example/generator/VideoGenerator.kt', 'w') as f:
    f.write(content)
