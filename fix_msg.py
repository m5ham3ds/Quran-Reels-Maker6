with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'Enter your own Gemini API Key.',
    'Enter your own API Key.'
)

with open('app/src/main/java/com/example/ui/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
