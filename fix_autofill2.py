import re

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val textStr = root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")',
    'val textStr = if (aiPlatform == "HuggingFace") root.getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content") else root.getJSONArray("candidates").getJSONObject(0).getJSONObject("content").getJSONArray("parts").getJSONObject(0).getString("text")'
)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
print("Replaced parsed")
