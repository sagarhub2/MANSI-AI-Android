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
    "Jarvis Code": "MANSI Code",
    "JARVIS CODE": "MANSI CODE",
    "Jarvis Pro": "MANSI AI",
    "JARVIS PRO": "MANSI AI",
    "JARVIS Pro": "MANSI AI",
    "Jarvis Pro Voice": "MANSI AI Voice",
    "JARVIS PRO VOICE": "MANSI AI VOICE",
    "Jarvis AI": "MANSI AI",
    "JARVIS AI": "MANSI AI",
    "Jarvis Intelligence": "MANSI AI",
    "JARVIS INTELLIGENCE": "MANSI AI",
}
for brand_path in root.rglob("*"):
    if not brand_path.is_file() or brand_path.suffix.lower() not in {".xml", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    # Manifest android:name entries are executable class identifiers; never rewrite them.
    if brand_path.name == "AndroidManifest.xml":
        continue
    # Theme/style resource names are identifiers, not visible UI labels. Replacing
    # Jarvis in themes.xml creates invalid Android resource names and breaks builds.
    if "/res/values/" in brand_path.as_posix() and brand_path.suffix.lower() == ".xml":
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
    # Explicitly clean visible product labels found during the screen review.
    extra_visible_replacements = {
        "JARVIS App Identity": "MANSI AI App Identity",
        "Jarvis App Identity": "MANSI AI App Identity",
        "Jarvis updates & announcements": "MANSI AI updates & announcements",
        "JARVIS updates & announcements": "MANSI AI updates & announcements",
        "JARVIS OFF • TAP TO START": "MANSI AI OFF • TAP TO START",
        "JARVIS INTELLIGENCE OS": "MANSI AI",
        "Jarvis Pro": "MANSI AI",
        "JARVIS PRO": "MANSI AI",
        "JARVIS Pro": "MANSI AI",
        "Jarvis Code": "MANSI Code",
        "JARVIS CODE": "MANSI CODE",
        "Official application ID: com.jarvis.assistant": "MANSI AI Android application",
    }
    for old_label, new_label in extra_visible_replacements.items():
        updated_brand_text = updated_brand_text.replace(old_label, new_label)
    for index, token in enumerate(protected_tokens):
        updated_brand_text = updated_brand_text.replace(f"__MANSI_PROTECTED_{index}__", token)
    if updated_brand_text != brand_text:
        brand_path.write_text(updated_brand_text, encoding="utf-8")
        print("Updated visible Jarvis branding in " + str(brand_path))


# Final visible-brand sweep: remove remaining Jarvis wording from quoted UI
# strings, while preserving Android package/class references and resource IDs.
def replace_jarvis_in_literal(match):
    quote, value = match.group(1), match.group(2)
    if value.startswith(("com.jarvis.", "com/Jarvis/", "@+id/", "@id/", "@string/", "@drawable/", "@mipmap/")):
        return match.group(0)
    value = re.sub(r"(?i)jarvis(?:\s+|[·•]\s*)code", "MANSI Code", value)
    value = re.sub(r"(?i)jarvis", "MANSI AI", value)
    return quote + value + quote

# Disabled: broad source-literal rewriting was corrupting Kotlin syntax.
# Explicit resource/UI replacements above are safer; keep package/class identifiers intact.
for safe_path in []:
    if not safe_path.is_file() or safe_path.suffix.lower() not in {".kt", ".java", ".xml", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if safe_path.name == "AndroidManifest.xml":
        continue
    if "/res/values/" in safe_path.as_posix() and safe_path.suffix.lower() == ".xml" and safe_path.name != "strings.xml":
        continue
    try:
        safe_text = safe_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    protected = []
    def protect_android_identifier(match):
        protected.append(match.group(0))
        return f"__MANSI_KEEP_{len(protected) - 1}__"
    cleaned = re.sub(
        r"""(?:android:id\s*=\s*["'][^"']+["']|@\+?id/[A-Za-z0-9_]+|R\.id\.[A-Za-z0-9_]+|binding\.[A-Za-z0-9_]+)""",
        protect_android_identifier,
        safe_text
    )
    for old_label, new_label in [
        ("JARVIS CODE", "MANSI CODE"), ("Jarvis Code", "MANSI Code"),
        ("Jarvis code", "MANSI Code"), ("JARVIS PRO", "MANSI AI"),
        ("Jarvis Pro", "MANSI AI"), ("JARVIS AI", "MANSI AI"),
        ("Jarvis AI", "MANSI AI"), ("JARVIS", "MANSI AI"),
        ("Jarvis", "MANSI AI"),
    ]:
        cleaned = cleaned.replace(old_label, new_label)
    cleaned = cleaned.replace("com.MANSI AI.", "com.jarvis.")
    cleaned = cleaned.replace("com/MANSI AI/", "com/Jarvis/")
    for index, token in enumerate(protected):
        cleaned = cleaned.replace(f"__MANSI_KEEP_{index}__", token)
    if cleaned != safe_text:
        safe_path.write_text(cleaned, encoding="utf-8")
        print("Cleaned remaining visible Jarvis text in " + str(safe_path))

# Disabled legacy cross-line regex sweep; it corrupts Kotlin source.
for sweep_path in []:
    if not sweep_path.is_file() or sweep_path.suffix.lower() not in {".xml", ".kt", ".java", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    # Manifest class names are quoted strings but must never be rebranded.
    if sweep_path.name == "AndroidManifest.xml":
        continue
    # Never rewrite Android theme resource identifiers; spaces make resource names invalid.
    if "/res/values/" in sweep_path.as_posix() and sweep_path.suffix.lower() == ".xml":
        continue
    try:
        sweep_text = sweep_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    # Restrict changes to quoted literals; don't rename Kotlin/Java identifiers.
    swept = re.sub(r"""(["\'])(.*?)(\1)""", replace_jarvis_in_literal, sweep_text, flags=re.S)
    if swept != sweep_text:
        sweep_path.write_text(swept, encoding="utf-8")
        print("Removed remaining Jarvis wording from string literals in " + str(sweep_path))

# Targeted cleanup of visible branding in source text. Preserve package names,
# resource IDs, and all unquoted identifiers to avoid breaking Android builds.
def clean_visible_string(match):
    quote = match.group(1)
    value = match.group(2)
    low = value.lower()
    if low.startswith(("com.jarvis.", "com/jarvis/", "com.jarvis", "@+id/", "@id/", "@string/", "@drawable/", "@mipmap/")):
        return match.group(0)
    value = re.sub(r"(?i)jarvis\\s*(?:[·•-]\\s*)?code", "MANSI Code", value)
    value = re.sub(r"(?i)jarvis", "MANSI AI", value)
    return quote + value + quote

for final_path in root.rglob("*"):
    if not final_path.is_file() or final_path.suffix.lower() not in {".kt", ".java", ".xml", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if final_path.name == "AndroidManifest.xml":
        continue
    if "/res/values/" in final_path.as_posix() and final_path.suffix.lower() == ".xml" and final_path.name != "strings.xml":
        continue
    try:
        final_text = final_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    # Only single-line string literals; never rewrite Kotlin identifiers or multiline code.
    final_clean = re.sub(r"""(["'])([^"'\\n]*)\\1""", clean_visible_string, final_text)
    if final_clean != final_text:
        final_path.write_text(final_clean, encoding="utf-8")
        print("Final visible brand cleanup: " + str(final_path))


# FIX: Generate every launcher icon from the actual MANSI logo, including
# Android adaptive icons (Android 8+) and legacy density icons.
# Pillow is installed by the workflow before this script runs.
from PIL import Image, ImageOps, ImageDraw

res = root / "res"
logo_path = res / "drawable/ic_jarvis_logo.png"
if not logo_path.exists():
    raise SystemExit(f"Cannot create launcher icons: missing {logo_path}")

logo = Image.open(logo_path).convert("RGBA")
# Crop to square, then place the full logo within Android's adaptive safe zone.
side = min(logo.size)
left = (logo.width - side) // 2
top = (logo.height - side) // 2
logo = logo.crop((left, top, left + side, top + side))

# Adaptive foreground canvas is 108dp; keep key art within the central 66dp.
adaptive = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
art = ImageOps.contain(logo, (264, 264), method=Image.Resampling.LANCZOS)
adaptive.alpha_composite(art, ((432 - art.width) // 2, (432 - art.height) // 2))
(res / "mipmap-anydpi-v26").mkdir(parents=True, exist_ok=True)
for density, size in [("mdpi",108),("hdpi",162),("xhdpi",216),("xxhdpi",324),("xxxhdpi",432)]:
    folder = res / f"mipmap-{density}"
    folder.mkdir(parents=True, exist_ok=True)
    foreground = adaptive.resize((size,size), Image.Resampling.LANCZOS)
    foreground.save(folder / "ic_launcher_foreground.png")
    # Legacy icons use a solid deep-purple background with the logo centered.
    legacy = Image.new("RGBA", (size,size), (16, 10, 40, 255))
    legacy_art = ImageOps.contain(logo, (int(size*0.78), int(size*0.78)), method=Image.Resampling.LANCZOS)
    legacy.alpha_composite(legacy_art, ((size-legacy_art.width)//2, (size-legacy_art.height)//2))
    legacy.save(folder / "ic_launcher.png")
    legacy.save(folder / "ic_launcher_round.png")

# Ensure the referenced adaptive background color resource exists.
values_dir = res / "values"
values_dir.mkdir(parents=True, exist_ok=True)
colors_xml = values_dir / "ic_launcher_background.xml"
colors_xml.write_text('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#100A28</color>
</resources>
''', encoding="utf-8")

for filename in ["ic_launcher.xml", "ic_launcher_round.xml"]:
    xml_path = res / "mipmap-anydpi-v26" / filename
    xml_path.write_text('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
''', encoding="utf-8")
print("FIXED launcher icons: MANSI logo generated for all legacy densities and adaptive foreground.")


# Force the launcher activity/application to reference the generated launcher icons.
manifest = root / "AndroidManifest.xml"
if not manifest.exists():
    raise SystemExit(f"Missing Android manifest: {manifest}")
manifest_text = manifest.read_text(encoding="utf-8")
if 'android:icon="@mipmap/ic_launcher"' not in manifest_text:
    manifest_text = re.sub(r'<application\b', '<application android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher_round"', manifest_text, count=1)
else:
    manifest_text = re.sub(r'android:roundIcon="[^"]+"', 'android:roundIcon="@mipmap/ic_launcher_round"', manifest_text, count=1)
    if 'android:roundIcon=' not in manifest_text:
        manifest_text = manifest_text.replace('android:icon="@mipmap/ic_launcher"', 'android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher_round"', 1)
manifest.write_text(manifest_text, encoding="utf-8")
print("Verified launcher manifest references MANSI-generated ic_launcher resources.")
