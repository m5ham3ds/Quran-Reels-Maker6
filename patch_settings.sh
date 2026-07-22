sed -i 's/import androidx.compose.material.icons.filled.Info/import androidx.compose.material.icons.filled.Info\nimport androidx.compose.material.icons.filled.Edit/g' app/src/main/java/com/example/ui/settings/SettingsScreen.kt

sed -i '/var logsList by remember { mutableStateOf(emptyList<String>()) }/a\
    var showKeywordPromptDialog by remember { mutableStateOf(false) }\
    val backgroundKeywordsPrompt by settingsManager.backgroundKeywordsPrompt.collectAsState(initial = "")' app/src/main/java/com/example/ui/settings/SettingsScreen.kt

