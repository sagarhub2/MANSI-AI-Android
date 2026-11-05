from pathlib import Path

ROOT = Path("source/mansi/app/src/main")

def edit(path, replacements):
    if not path.is_file():
        print(f"WARNING: optional optimization target missing; skipped: {path}")
        return
    before = path.read_text(encoding="utf-8")
    after = before
    for old, new in replacements:
        if old not in after:
            if new in after:
                print(f"Already applied: {path}")
            else:
                print(f"WARNING: source pattern not found; skipped safely in {path}: {old[:90]!r}")
            continue
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
            return selected
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

print("MANSI optimization pass finished. Review WARNING lines; Gradle remains the build validation.")
