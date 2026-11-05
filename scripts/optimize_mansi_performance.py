from pathlib import Path

ROOT = Path("source/mansi/app/src/main")
required = [
    ROOT / "java/com/jarvis/assistant/audio/AudioPlayer.kt",
    ROOT / "java/com/jarvis/assistant/data/model/GeminiLiveModels.kt",
    ROOT / "java/com/jarvis/assistant/data/preferences/AppPreferences.kt",
    ROOT / "java/com/jarvis/assistant/ui/settings/PersonaActivity.kt",
    ROOT / "res/layout/activity_persona.xml",
]
missing = [str(p) for p in required if not p.is_file()]
if missing:
    raise SystemExit("Required MANSI source files missing: " + ", ".join(missing))

def edit(path, replacements):
    before = path.read_text(encoding="utf-8")
    after = before
    for old, new in replacements:
        if old not in after:
            if new in after:
                continue
            raise SystemExit(f"Expected source pattern not found in {path}: {old[:90]!r}")
        after = after.replace(old, new, 1)
    if after != before:
        path.write_text(after, encoding="utf-8")
        print("Updated:", path)

audio = ROOT / "java/com/jarvis/assistant/audio/AudioPlayer.kt"
edit(audio, [
    ("// 2. If Gemini is still generating (turnComplete not yet received): wait 40 cycles (~800ms)",
     "// 2. If Gemini has not signaled completion: cap the idle gap at 25 cycles (~500ms)."),
    ("(silenceCounter >= 40)", "(silenceCounter >= 25)"),
])

models = ROOT / "java/com/jarvis/assistant/data/model/GeminiLiveModels.kt"
edit(models, [
    ('const val DEFAULT_VOICE = "Puck"', 'const val DEFAULT_VOICE = "Aoede"'),
])

prefs = ROOT / "java/com/jarvis/assistant/data/preferences/AppPreferences.kt"
edit(prefs, [
    ('get() = prefs.getString(KEY_VOICE, GeminiConstants.DEFAULT_VOICE) ?: GeminiConstants.DEFAULT_VOICE',
     '''get() {
            val stored = prefs.getString(KEY_VOICE, GeminiConstants.DEFAULT_VOICE)
            // Migrate previous Puck/Kore defaults to MANSI's selected cute feminine voice.
            val selected = if (stored.equals("Puck", ignoreCase = true) ||
                stored.equals("Kore", ignoreCase = true)) "Aoede"
            else stored ?: GeminiConstants.DEFAULT_VOICE
            if (selected != stored) prefs.edit().putString(KEY_VOICE, selected).apply()
            selected
        }'''),
])

persona = ROOT / "java/com/jarvis/assistant/ui/settings/PersonaActivity.kt"
edit(persona, [
    ('GeminiConstants.PERSONALITY_TECHGPT_X -> selectVoice("Puck")',
     'GeminiConstants.PERSONALITY_TECHGPT_X -> selectVoice("Aoede")'),
    ('else -> binding.rbVoicePuck.isChecked = true',
     'else -> binding.rbVoiceAoede.isChecked = true'),
    ('else -> "Puck"', 'else -> "Aoede"'),
])

layout = ROOT / "res/layout/activity_persona.xml"
edit(layout, [
    ('Aoede (Warm, expressive female voice)', 'Aoede (Cute, warm expressive female voice)'),
])

print("MANSI performance + cute female voice patch verified.")
