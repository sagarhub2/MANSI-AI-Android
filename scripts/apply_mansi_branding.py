from pathlib import Path

root = Path("source/mansi/app/src/main")
layout = root / "res/layout/fragment_home.xml"
xml = layout.read_text(encoding="utf-8")
old = '''        <ImageView
            android:id="@+id/ivHeaderJarvisLogo"
            android:layout_width="110dp"
            android:layout_height="34dp"
            android:src="@drawable/ic_jarvis_logo"
            android:scaleType="fitCenter"
            android:contentDescription="Jarvis Logo" />

        <TextView
            android:id="@+id/tvGreeting"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Welcome, Rehaan"
            android:textColor="?attr/themeTextPrimary"
            android:textSize="14sp"
            android:textStyle="bold"
            android:fontFamily="sans-serif-medium"
            android:layout_marginTop="2dp" />'''
new = '''        <TextView
            android:id="@+id/tvHeaderBrand"
            android:layout_width="wrap_content"
            android:layout_height="34dp"
            android:gravity="center"
            android:text="MANSI AI"
            android:textColor="?attr/themeTextPrimary"
            android:textSize="22sp"
            android:textStyle="bold"
            android:letterSpacing="0.08"
            android:fontFamily="sans-serif-black"
            android:contentDescription="MANSI AI" />

        <TextView
            android:id="@+id/tvGreeting"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Your Assistant"
            android:textColor="?attr/themeTextPrimary"
            android:textSize="14sp"
            android:textStyle="bold"
            android:fontFamily="sans-serif-medium"
            android:layout_marginTop="2dp" />'''
if old not in xml:
    raise SystemExit("Expected home header XML not found; stopping without changing files.")
layout.write_text(xml.replace(old, new, 1), encoding="utf-8")

kt = root / "java/com/jarvis/assistant/ui/home/HomeFragment.kt"
src = kt.read_text(encoding="utf-8")
old_logic = '''        val userName = preferences.userName.ifBlank { "Rehaan" }
        val hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY)
        val timeGreeting = when (hour) {
            in 4..11 -> "Good morning"
            in 12..16 -> "Good afternoon"
            in 17..21 -> "Good evening"
            else -> "Welcome back"
        }
        binding.tvGreeting.text = "$timeGreeting, $userName"'''
new_logic = '''        // Keep the requested fixed product tagline instead of a personalized time greeting.
        binding.tvGreeting.text = "Your Assistant"'''
if old_logic not in src:
    raise SystemExit("Expected home greeting logic not found; stopping without changing files.")
kt.write_text(src.replace(old_logic, new_logic, 1), encoding="utf-8")

strings = root / "res/values/strings.xml"
s = strings.read_text(encoding="utf-8")
if '<string name="app_name">MANSI AI</string>' not in s:
    raise SystemExit("App label is not MANSI AI; stopping.")
print("Applied MANSI AI home brand and Your Assistant subtitle.")


# Rebrand profile labels and primary-user display text.
profile_replacements = {
    "TechGPT X": "Sagar",
    "TechGPTX": "Sagar",
    "Jarvis Operator": "MANSI AI User",
    "JARVIS OPERATOR": "MANSI AI USER",
    "Primary User": "MANSI AI User",
    "PRIMARY USER": "MANSI AI USER",
}
text_suffixes = {".xml", ".kt", ".java", ".html", ".js", ".json", ".txt", ".properties"}
changed = []
for path in root.rglob("*"):
    if path.is_file() and path.suffix.lower() in text_suffixes:
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = original
        for old_text, new_text in profile_replacements.items():
            updated = updated.replace(old_text, new_text)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path))
if not changed:
    print("NOTE: No matching profile labels were found in source text files.")
else:
    print("Updated profile branding in: " + ", ".join(changed))


# Set the owner's social profile links and remove old YouTube profile links.
import re

settings_kt = root / "java/com/jarvis/assistant/ui/settings/SettingsFragment.kt"
if settings_kt.exists():
    src = settings_kt.read_text(encoding="utf-8")
    src = src.replace("https://www.instagram.com/techgptx.ai", "https://instagram.com/hyee__sagar")
    src = re.sub(
        r'binding\.btnSocialTelegram\.setOnClickListener \{.*?\n        \}',
        'binding.btnSocialTelegram.setOnClickListener {\n            openUrl("https://t.me/H_sagarr")\n        }',
        src, count=1, flags=re.S
    )
    # Hide the old YouTube profile shortcut; leave YouTube automation features untouched.
    if "binding.btnSocialYoutube.visibility = View.GONE" not in src:
        src = src.replace(
            "binding.btnSocialYoutube.setOnClickListener {",
            "binding.btnSocialYoutube.visibility = View.GONE\n        binding.btnSocialYoutube.setOnClickListener {",
            1
        )
    settings_kt.write_text(src, encoding="utf-8")

privacy_kt = root / "java/com/jarvis/assistant/ui/settings/PrivacyShieldActivity.kt"
if privacy_kt.exists():
    src = privacy_kt.read_text(encoding="utf-8")
    if "import android.view.View" not in src:
        src = src.replace("package com.jarvis.assistant.ui.settings\n", "package com.jarvis.assistant.ui.settings\n\nimport android.view.View\n", 1)
    src = src.replace("https://www.instagram.com/techgptx.ai", "https://instagram.com/hyee__sagar")
    src = re.sub(
        r'binding\.btnJoinOfficialTelegram\.setOnClickListener \{.*?\n        \}',
        'binding.btnJoinOfficialTelegram.setOnClickListener {\n            openUrl("https://t.me/H_sagarr")\n        }',
        src, count=1, flags=re.S
    )
    src = re.sub(
        r'binding\.btnJoinTelegram\.setOnClickListener \{.*?\n        \}',
        'binding.btnJoinTelegram.setOnClickListener {\n            openUrl("https://t.me/H_sagarr")\n        }',
        src, count=1, flags=re.S
    )
    if "binding.btnJoinYoutube.visibility = View.GONE" not in src:
        src = src.replace(
            "binding.btnJoinYoutube.setOnClickListener {",
            "binding.btnJoinYoutube.visibility = View.GONE\n        binding.btnJoinYoutube.setOnClickListener {",
            1
        )
    privacy_kt.write_text(src, encoding="utf-8")
print("Applied personal Instagram/Telegram links and hid old YouTube profile shortcuts.")

# Prefer a feminine voice in Gemini Live configuration where the project exposes
# a voiceName setting. Gemini Live supports voice names such as Aoede and Kore;
# use Kore as the default feminine-sounding voice without changing model/API flow.
models_kt = root / "java/com/jarvis/assistant/data/model/GeminiLiveModels.kt"
if models_kt.exists():
    src = models_kt.read_text(encoding="utf-8")
    import re
    # Patch only explicit voiceName assignments/defaults; avoid guessing at unrelated code.
    # The actual project default is DEFAULT_VOICE = "Puck" (a masculine-sounding voice).
    # Force the app's default Live voice to Kore, and keep any explicit voiceName
    # defaults aligned with it. The live socket sends preferences.voice as voice_name.
    updated = re.sub(
        r'(?m)(const\s+val\s+DEFAULT_VOICE\s*=\s*["\'])([^"\']+)(["\'])',
        r'\g<1>Kore\3',
        src
    )
    updated = re.sub(
        r"""(voiceName\s*[:=]\s*["'])(?:Aoede|Puck|Charon|Fenrir|Leda|Orus|Zephyr|Kore)(["'])""",
        r"\g<1>Kore\2",
        updated
    )
    if updated != src:
        models_kt.write_text(updated, encoding="utf-8")
        print("Set Gemini Live DEFAULT_VOICE/voiceName to Kore (female voice).")
    else:
        print("WARNING: GeminiLiveModels voice defaults were not changed; inspect source.")


# Enforce a cute, feminine voice for Gemini Live voice defaults.
# Migrate the old masculine Puck default where a source file clearly refers to voice.
for const_path in root.rglob("*"):
    if not const_path.is_file() or const_path.suffix.lower() not in {".kt", ".java", ".xml", ".json", ".txt"}:
        continue
    try:
        voice_src = const_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    voice_updated = voice_src
    if "voice" in voice_src.lower() or "voice_name" in voice_src.lower() or "DEFAULT_VOICE" in voice_src:
        voice_updated = re.sub(r'(?i)(DEFAULT_VOICE\s*=\s*["\'])Puck(["\'])', r'\1Kore\2', voice_updated)
        voice_updated = re.sub(r'(?i)(voiceName\s*[:=]\s*["\'])Puck(["\'])', r'\1Kore\2', voice_updated)
    if voice_updated != voice_src:
        const_path.write_text(voice_updated, encoding="utf-8")
        print("Migrated masculine Puck voice default in " + str(const_path))

# Make every voice selector entry use a supported feminine voice.
for voice_path in root.rglob("*"):
    if not voice_path.is_file() or voice_path.suffix.lower() not in {".kt", ".java", ".xml", ".json", ".txt"}:
        continue
    try:
        voice_text = voice_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    revised = voice_text
    revised = revised.replace("Fenrir (Deep, protective charismatic male voice)", "Kore (Cute, gentle female voice)")
    revised = revised.replace("Puck (Crisp, modern dynamic male voice)", "Aoede (Cute, playful female voice)")
    revised = revised.replace("Charon (Distinguished butler male voice)", "Kore (Soft, sweet female voice)")
    revised = revised.replace("Deep, protective charismatic male voice", "Cute, gentle female voice")
    revised = revised.replace("Crisp, modern dynamic male voice", "Cute, playful female voice")
    revised = revised.replace("Distinguished butler male voice", "Soft, sweet female voice")
    if revised != voice_text:
        voice_path.write_text(revised, encoding="utf-8")
        print("Updated female-only voice labels in " + str(voice_path))


# Replace visible Jarvis chat branding while keeping Java/Kotlin package names intact.
visible_brand_replacements = {
    "Jarvis • Gemini Live • Active": "MANSI AI • Gemini Live • Active",
    "Jarvis · Gemini Live · Active": "MANSI AI · Gemini Live · Active",
    "Message Jarvis": "Message MANSI AI",
    "Message JARVIS": "Message MANSI AI",
    "Jarvis Code": "MANSI AI Code",
    "JARVIS CODE": "MANSI AI CODE",
}
for brand_path in root.rglob("*"):
    if not brand_path.is_file() or brand_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".txt", ".properties"}:
        continue
    # Theme/style resource names are identifiers, not visible UI labels. Replacing
    # Jarvis in themes.xml creates invalid Android resource names and breaks builds.
    if brand_path.as_posix().endswith("/res/values/themes.xml"):
        continue
    try:
        brand_text = brand_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    updated_brand_text = brand_text
    # Protect Android resource IDs and code identifiers before changing visible labels.
    protected_tokens = []
    def protect_token(match):
        protected_tokens.append(match.group(0))
        return f"__MANSI_PROTECTED_{len(protected_tokens) - 1}__"
    updated_brand_text = re.sub(
        r"""(?:android:id\s*=\s*["'][^"']+["']|@\+?id/[A-Za-z0-9_]+|R\.id\.[A-Za-z0-9_]+|binding\.[A-Za-z0-9_]+)""",
        protect_token,
        updated_brand_text
    )
    for old_label, new_label in visible_brand_replacements.items():
        updated_brand_text = updated_brand_text.replace(old_label, new_label)
    for index, token in enumerate(protected_tokens):
        updated_brand_text = updated_brand_text.replace(f"__MANSI_PROTECTED_{index}__", token)
    if updated_brand_text != brand_text:
        brand_path.write_text(updated_brand_text, encoding="utf-8")
        print("Updated visible Jarvis branding in " + str(brand_path))
