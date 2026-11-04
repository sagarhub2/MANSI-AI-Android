from pathlib import Path

ROOT = Path("source/mansi/app/src/main")

def patch(rel, old, new):
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"Roast Mode patch: missing {path}")
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Roast Mode patch: expected source block not found in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

patch("java/com/jarvis/assistant/data/preferences/AppPreferences.kt",
'''        private const val KEY_CUSTOM_ENDPOINT = "key_custom_endpoint"''',
'''        private const val KEY_CUSTOM_ENDPOINT = "key_custom_endpoint"
        private const val KEY_ROAST_MODE_ENABLED = "key_roast_mode_enabled"
        private const val KEY_ROAST_MODE_LEVEL = "key_roast_mode_level"''')

patch("java/com/jarvis/assistant/data/preferences/AppPreferences.kt",
'''    var isSilentExecutionMode: Boolean
        get() = prefs.getBoolean(KEY_SILENT_EXECUTION_MODE, false)''',
'''    var isRoastModeEnabled: Boolean
        get() = prefs.getBoolean(KEY_ROAST_MODE_ENABLED, false)
        set(value) = prefs.edit().putBoolean(KEY_ROAST_MODE_ENABLED, value).apply()

    var roastModeLevel: String
        get() = prefs.getString(KEY_ROAST_MODE_LEVEL, "Funny") ?: "Funny"
        set(value) = prefs.edit().putString(KEY_ROAST_MODE_LEVEL, value.takeIf { it in setOf("Cute", "Funny", "Savage", "Extreme") } ?: "Funny").apply()

    var isSilentExecutionMode: Boolean
        get() = prefs.getBoolean(KEY_SILENT_EXECUTION_MODE, false)''')

patch("java/com/jarvis/assistant/util/PromptGenerator.kt",
'''        isSilentExecutionMode: Boolean = false
    ): String {''',
'''        isSilentExecutionMode: Boolean = false,
        isRoastModeEnabled: Boolean = false,
        roastModeLevel: String = "Funny"
    ): String {''')

patch("java/com/jarvis/assistant/util/PromptGenerator.kt",
'''$personalityInstruction

$languageInstruction''',
'''$personalityInstruction

${if (isRoastModeEnabled) """
[ROAST MODE: ON — LEVEL: $roastModeLevel]
- Respond in playful, original Hinglish roasts with witty timing; tailor jokes to the user's actual message, not identity assumptions.
- Cute: gentle teasing. Funny: light punchlines. Savage: sharper but friendly banter. Extreme: theatrical, cheeky exaggeration without cruelty.
- Keep it consensual and fun. Never target protected traits, disability, trauma, body/appearance, poverty, family tragedy, or sensitive personal information. No threats, slurs, harassment, or genuine humiliation.
- If the user says stop, seems hurt, or asks for normal help, immediately drop the roast and respond supportively. Never roast a third party based on sensitive traits.
- Do not repeat canned jokes; keep replies concise and conversational. Normal assistant behavior resumes when Roast Mode is OFF.
""".trimIndent() else ""}

$languageInstruction''')

patch("java/com/jarvis/assistant/background/JarvisConversationService.kt",
'''                isSilentExecutionMode = preferences.isSilentExecutionMode
            )''',
'''                isSilentExecutionMode = preferences.isSilentExecutionMode,
                isRoastModeEnabled = preferences.isRoastModeEnabled,
                roastModeLevel = preferences.roastModeLevel
            )''')

patch("java/com/jarvis/assistant/background/JarvisConversationService.kt",
'''            instance.liveWebSocket?.sendClientContent(text)
            JarvisApp.instance.chatRepository.addTurn(text, "")''',
'''            val prefs = JarvisApp.instance.preferences
            val outgoing = if (prefs.isRoastModeEnabled) {
                "[ROAST MODE ON — ${prefs.roastModeLevel}] Keep this reply playful, original, consensual Hinglish banter. Avoid sensitive traits, appearance, trauma, slurs, threats or humiliation; stop immediately if asked. User message: $text"
            } else text
            instance.liveWebSocket?.sendClientContent(outgoing)
            JarvisApp.instance.chatRepository.addTurn(text, "")''')

patch("java/com/jarvis/assistant/ui/chat/ChatFragment.kt",
'''        binding.chipMode.setOnClickListener {
            Toast.makeText(requireContext(), "Mode: Code & Assistant", Toast.LENGTH_SHORT).show()
        }''',
'''        updateRoastModeChip()
        binding.chipMode.setOnClickListener { showRoastModeDialog() }''')

patch("java/com/jarvis/assistant/ui/chat/ChatFragment.kt",
'''    private fun sendMessage() {''',
'''    private fun updateRoastModeChip() {
        val prefs = JarvisApp.instance.preferences
        val label = if (prefs.isRoastModeEnabled) "🔥 ${prefs.roastModeLevel}" else "Roast OFF"
        binding.chipMode.findViewById<android.widget.TextView>(com.jarvis.assistant.R.id.tvRoastModeLabel)?.text = label
    }

    private fun showRoastModeDialog() {
        val prefs = JarvisApp.instance.preferences
        val levels = arrayOf("Cute", "Funny", "Savage", "Extreme")
        val selected = levels.indexOf(prefs.roastModeLevel).coerceAtLeast(0)
        AlertDialog.Builder(requireContext())
            .setTitle("🔥 MANSI Roast Mode")
            .setMessage("Choose your roast level. Roast Mode stays off until you turn it on.")
            .setSingleChoiceItems(levels, selected) { _, which ->
                prefs.roastModeLevel = levels[which]
            }
            .setPositiveButton("Turn ON") { _, _ ->
                prefs.isRoastModeEnabled = true
                updateRoastModeChip()
                Toast.makeText(requireContext(), "🔥 Roast Mode ON · ${prefs.roastModeLevel}", Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton(if (prefs.isRoastModeEnabled) "Turn OFF" else "Cancel") { _, _ ->
                if (prefs.isRoastModeEnabled) {
                    prefs.isRoastModeEnabled = false
                    updateRoastModeChip()
                    Toast.makeText(requireContext(), "Roast Mode OFF", Toast.LENGTH_SHORT).show()
                }
            }
            .setNeutralButton("Close", null)
            .show()
    }

    private fun sendMessage() {''')

patch("res/layout/fragment_chat.xml",
'''            android:text="Jarvis • Gemini Live • Active"''',
'''            android:text="MANSI AI • Gemini Live • Active"''')
patch("res/layout/fragment_chat.xml",
'''            android:hint="Message Jarvis"''',
'''            android:hint="Message MANSI AI"''')
patch("res/layout/fragment_chat.xml",
'''                    android:text="Code"''',
'''                    android:id="@+id/tvRoastModeLabel"
                    android:text="Roast OFF"''')
print("Roast Mode source patch applied.")
