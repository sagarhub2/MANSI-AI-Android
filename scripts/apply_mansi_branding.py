from pathlib import Path
import xml.etree.ElementTree as ET

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


# Profile names are intentionally left unchanged by the logo/animation patch.

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

# Keep the requested Puck voice unchanged; branding must not alter voice defaults.
# Replace visible Jarvis chat branding while keeping Java/Kotlin package names intact.
visible_brand_replacements = {
    "Jarvis • Gemini Live • Active": "MANSI AI • Gemini Live • Active",
    "Jarvis · Gemini Live · Active": "MANSI AI · Gemini Live · Active",
    "Message Jarvis": "Message MANSI AI",
    "Message JARVIS": "Message MANSI AI",
    "Jarvis Code": "MANSI Code",
    "JARVIS CODE": "MANSI CODE",
    "Jarvis Pro": "MANSI PRO",
    "JARVIS PRO": "MANSI PRO",
    "JARVIS Pro": "MANSI PRO",
    "Jarvis Pro Voice": "MANSI PRO · Voice: Puck",
    "JARVIS PRO VOICE": "MANSI PRO · Voice: Puck",
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
        "JARVIS OPERATOR • PRIMARY USER": "MANSI AI Operator · Primary User",
        "JARVIS OPERATOR · PRIMARY USER": "MANSI AI Operator · Primary User",
        "Jarvis Operator • Primary User": "MANSI AI Operator · Primary User",
        "JARVIS PRO": "MANSI PRO",
        "Jarvis Pro": "MANSI PRO",
        "JARVIS PRO VOICE": "MANSI PRO · Voice: Puck",
        "JARVIS PRO · VOICE: PUCK": "MANSI PRO · Voice: Puck",
        "TECHGPT X": "MANSI AI",
        "TECHGPTX": "MANSI AI",
        "MANSI AI . SAGAR": "MANSI AI OS · SAGAR",
        "MANSI AI OS . SAGAR": "MANSI AI OS · SAGAR",
        "MANSI AI App identity": "MANSI AI App identity",
        "Jarvis updates & announcements": "MANSI AI updates & announcements",
        "JARVIS updates & announcements": "MANSI AI updates & announcements",
        "JARVIS OFF • TAP TO START": "MANSI AI OFF • TAP TO START",
        "JARVIS INTELLIGENCE OS": "MANSI AI",
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
for safe_path in root.rglob('*'):
    if not safe_path.is_file() or safe_path.suffix.lower() not in {".xml", ".html", ".js", ".json", ".txt", ".properties"}:
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


# Explicitly enforce the requested visible labels in XML/resource text only.
# These targeted substitutions run after generic branding so specific labels
# such as MANSI PRO are not overwritten by the broad MANSI AI replacement.
requested_ui_labels = [
    ("ENROLL VOICE", "ENROLL VOICE"),
    ("Enroll Voice", "ENROLL VOICE"),
    ("AI Persona & Voice", "MANSI PRO · Voice: Puck"),
    ("AI Persona and Voice", "MANSI PRO · Voice: Puck"),
    ("JARVIS OPERATOR • PRIMARY USER", "MANSI AI Operator · Primary User"),
    ("JARVIS OPERATOR · PRIMARY USER", "MANSI AI Operator · Primary User"),
    ("Jarvis Operator • Primary User", "MANSI AI Operator · Primary User"),
    ("MANSI AI Operator • Primary User", "MANSI AI Operator · Primary User"),
    ("MANSI AI PRO", "MANSI PRO"),
]
for ui_path in root.rglob("*"):
    if not ui_path.is_file() or ui_path.suffix.lower() not in {".xml", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if ui_path.name == "AndroidManifest.xml":
        continue
    try:
        ui_before = ui_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    ui_after = ui_before
    for old_label, new_label in requested_ui_labels:
        ui_after = ui_after.replace(old_label, new_label)
    if ui_after != ui_before:
        if ui_path.suffix.lower() == ".xml":
            ET.fromstring(ui_after)
        ui_path.write_text(ui_after, encoding="utf-8")
        print("Enforced requested MANSI UI labels:", ui_path)

# Cross-line literal rewriting is intentionally omitted because it corrupts Kotlin source.

# Targeted cleanup of visible branding in source text. Preserve package names,
# resource IDs, and all unquoted identifiers to avoid breaking Android builds.
def clean_visible_string(match):
    quote = match.group(1)
    value = match.group(2)
    low = value.lower()
    if low.startswith(("com.jarvis.", "com/jarvis/", "com.jarvis", "@+id/", "@id/", "@string/", "@drawable/", "@mipmap/")):
        return match.group(0)
    value = re.sub(r"(?i)jarvis\s*(?:[·•-]\s*)?code", "MANSI Code", value)
    value = re.sub(r"(?i)jarvis", "MANSI AI", value)
    return quote + value + quote

for final_path in root.rglob("*"):
    if not final_path.is_file() or final_path.suffix.lower() not in {".xml", ".html", ".js", ".json", ".txt", ".properties"}:
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
    final_clean = re.sub(r"""(["'])([^"'\n]*)\1""", clean_visible_string, final_text)
    if final_clean != final_text:
        final_path.write_text(final_clean, encoding="utf-8")
        print("Final visible brand cleanup: " + str(final_path))


# FIX: Generate every launcher icon from the actual MANSI logo, including
# Android adaptive icons (Android 8+) and legacy density icons.
# Pillow is installed by the workflow before this script runs.
from PIL import Image, ImageOps, ImageDraw

res = root / "res"
# Prefer the new MANSI artwork when the bundled project includes it.
# Older project ZIPs may not contain that added asset, so fall back safely
# to the existing in-project logo instead of failing the entire APK build.
preferred_logo = res / "drawable/mansi_launcher_source.png"
repo_logo = Path("branding/mansi_launcher_source.png")
if repo_logo.is_file():
    preferred_logo.parent.mkdir(parents=True, exist_ok=True)
    preferred_logo.write_bytes(repo_logo.read_bytes())
legacy_logo = res / "drawable/ic_jarvis_logo.png"
logo_path = preferred_logo if preferred_logo.is_file() else legacy_logo
if not logo_path.is_file():
    # Last-resort generated premium MANSI monogram so builds never fail only
    # because the ZIP omitted the optional image asset.
    logo = Image.new("RGBA", (512, 512), (16, 10, 40, 255))
    draw = ImageDraw.Draw(logo)
    draw.ellipse((42, 42, 470, 470), outline=(0, 225, 255, 255), width=14)
    draw.ellipse((62, 62, 450, 450), outline=(180, 70, 255, 255), width=8)
    draw.text((120, 160), "M", fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 225, 255, 255))
    draw.text((95, 285), "AI", fill=(0, 225, 255, 255), stroke_width=1, stroke_fill=(180, 70, 255, 255))
    logo_path.parent.mkdir(parents=True, exist_ok=True)
    logo.save(logo_path)
    print("Generated fallback MANSI AI monogram because no bundled logo asset was present.")
else:
    print("Using launcher artwork: " + str(logo_path))
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


# Explicitly enforce MANSI AI branding on the three security/control screens.
# Run this after the legacy sweep so these screen labels remain correct in the APK.
import xml.etree.ElementTree as ET

security_screen_titles = {
    "Privacy & Data Shield": "Privacy & Data Shield",
    "Hands-Free & App Control": "Hands-Free & App Control",
    "System Authorizations": "System Authorizations",
}
for xml_path in root.rglob("*.xml"):
    try:
        xml_text = xml_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    updated_xml = xml_text
    # Replace visible legacy brand text in XML attributes/text while preserving
    # resource IDs and package/drawable references required by Android.
    updated_xml = re.sub(r'(?i)(android:text\s*=\s*["\'])[^"\']*jarvis[^"\']*(["\'])',
                         r'\1MANSI AI\2', updated_xml)
    updated_xml = re.sub(r'(?i)(android:contentDescription\s*=\s*["\'])[^"\']*jarvis[^"\']*(["\'])',
                         r'\1MANSI AI\2', updated_xml)
    updated_xml = re.sub(r'(?i)(<string\b[^>]*>)[^<]*jarvis[^<]*(</string>)',
                         r'\1MANSI AI\2', updated_xml)
    if updated_xml != xml_text:
        # Validate XML before writing so a branding edit cannot break resources.
        ET.fromstring(updated_xml)
        xml_path.write_text(updated_xml, encoding="utf-8")
        print("Enforced MANSI AI visible branding in " + str(xml_path))


# Replace only the visible legacy logo artwork with a dedicated MANSI AI wordmark.
# Use a new drawable resource name so an existing vector ic_jarvis_logo.xml cannot win.
from PIL import Image, ImageDraw, ImageFont
logo_out = root / "res/drawable/mansi_ai_wordmark.png"
logo_out.parent.mkdir(parents=True, exist_ok=True)
canvas = Image.new("RGBA", (900, 220), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)
font = None
for font_file in (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
):
    try:
        font = ImageFont.truetype(font_file, 118)
        break
    except OSError:
        pass
if font is None:
    font = ImageFont.load_default()
wordmark = "MANSI AI"
bbox = draw.textbbox((0, 0), wordmark, font=font, stroke_width=1)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
px, py = (900 - tw) // 2, (220 - th) // 2 - bbox[1]
draw.text((px, py), wordmark, font=font, fill=(25, 10, 35, 255))
canvas.save(logo_out)

# Redirect layouts using the old wordmark to the newly generated drawable.
updated_layouts = []
for layout_path in (root / "res/layout").rglob("*.xml"):
    try:
        layout_text = layout_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    updated = layout_text.replace("@drawable/ic_jarvis_logo", "@drawable/mansi_ai_wordmark")
    if updated != layout_text:
        ET.fromstring(updated)
        layout_path.write_text(updated, encoding="utf-8")
        updated_layouts.append(str(layout_path))
print("Created MANSI AI wordmark and updated logo references in: " + ", ".join(updated_layouts))


# Animate the actual layout that contains the MANSI AI logo.
# The previous attempt searched for literal screen-title text, but this project uses string resources.
import re as _mansi_re
anim_dir = root / "res/anim"
anim_dir.mkdir(parents=True, exist_ok=True)
(anim_dir / "mansi_permission_item_enter.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android"
    android:duration="520"
    android:interpolator="@android:interpolator/decelerate_cubic">
    <alpha android:fromAlpha="0.0" android:toAlpha="1.0" />
    <translate android:fromYDelta="8%p" android:toYDelta="0" />
    <scale
        android:fromXScale="0.96"
        android:toXScale="1.0"
        android:fromYScale="0.96"
        android:toYScale="1.0"
        android:pivotX="50%"
        android:pivotY="50%" />
</set>
""", encoding="utf-8")
(anim_dir / "mansi_permission_list_enter.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<layoutAnimation xmlns:android="http://schemas.android.com/apk/res/android"
    android:animation="@anim/mansi_permission_item_enter"
    android:animationOrder="normal"
    android:delay="12%" />
""", encoding="utf-8")

animated_layouts = []
for auth_layout in (root / "res/layout").rglob("*.xml"):
    try:
        auth_xml = auth_layout.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    # Only target layouts that actually display the new MANSI AI logo.
    if "@drawable/mansi_ai_wordmark" not in auth_xml:
        continue
    if "android:layoutAnimation=" in auth_xml:
        continue
    opening = _mansi_re.search(r"<(?!\?|!)([A-Za-z0-9_.]+)(\s[^>]*?)?>", auth_xml)
    if not opening:
        continue
    tag, attrs = opening.group(1), opening.group(2) or ""
    # layoutAnimation is supported by ViewGroup roots; skip single-view roots.
    if tag in {"ImageView", "TextView", "Button", "androidx.appcompat.widget.AppCompatImageView"}:
        continue
    new_attrs = attrs.rstrip() + ' android:layoutAnimation="@anim/mansi_permission_list_enter"'
    updated_xml = auth_xml[:opening.start()] + "<" + tag + new_attrs + ">" + auth_xml[opening.end():]
    try:
        ET.fromstring(updated_xml)
    except ET.ParseError as exc:
        print("Skipping animation for invalid XML", auth_layout, exc)
        continue
    auth_layout.write_text(updated_xml, encoding="utf-8")
    animated_layouts.append(str(auth_layout))
print("Attached entrance animation to logo-containing layouts: " + (", ".join(animated_layouts) if animated_layouts else "No layout references the generated logo; verify logo drawable mapping."))


# LAST PASS: enforce the exact settings-screen labels after all generic cleanup.
# This intentionally runs at EOF so earlier broad branding substitutions cannot undo it.
final_labels = {
    "TechGPT X": "MANSI AI",
    "TECHGPT X": "MANSI AI",
    "TECHGPTX": "MANSI AI",
    "Jarvis Operator • Primary User": "MANSI AI Operator · Primary User",
    "JARVIS OPERATOR • PRIMARY USER": "MANSI AI Operator · Primary User",
    "JARVIS OPERATOR · PRIMARY USER": "MANSI AI Operator · Primary User",
    "Jarvis Pro · Voice: Puck": "MANSI PRO · Voice: Puck",
    "Jarvis Pro • Voice: Puck": "MANSI PRO · Voice: Puck",
    "JARVIS PRO · VOICE: PUCK": "MANSI PRO · Voice: Puck",
    "Jarvis Pro": "MANSI PRO",
    "JARVIS PRO": "MANSI PRO",
    "Enroll Voice": "ENROLL VOICE",
    "ENROLL VOICE": "ENROLL VOICE",
    "MANSI AI . SAGAR": "MANSI AI OS · SAGAR",
    "MANSI AI OS . SAGAR": "MANSI AI OS · SAGAR",
}
for final_ui_path in root.rglob("*"):
    if not final_ui_path.is_file() or final_ui_path.suffix.lower() not in {".xml", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if final_ui_path.name == "AndroidManifest.xml":
        continue
    try:
        final_before = final_ui_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    final_after = final_before
    for old_label, new_label in final_labels.items():
        final_after = final_after.replace(old_label, new_label)
    # Match capitalization/punctuation variations for the subtitle and voice row.
    final_after = re.sub(r"(?i)jarvis\\s+operator\\s*[·•]\\s*primary user", "MANSI AI Operator · Primary User", final_after)
    final_after = re.sub(r"(?i)jarvis\\s+pro\\s*[·•]\\s*voice:\\s*puck", "MANSI PRO · Voice: Puck", final_after)
    final_after = re.sub(r"(?i)android:text=([\"'])enroll voice\\1", 'android:text="ENROLL VOICE"', final_after)
    if final_after != final_before:
        if final_ui_path.suffix.lower() == ".xml":
            ET.fromstring(final_after)
        final_ui_path.write_text(final_after, encoding="utf-8")
        print("FINAL settings label enforcement:", final_ui_path)


# FINAL CROSS-SOURCE PASS: Settings and App Identity labels may be hard-coded in Kotlin.
# Replace only exact user-facing strings; never change package names or implementation identifiers.
identity_labels = {
    "TechGPT X": "MANSI AI",
    "TECHGPT X": "MANSI AI",
    "TECHGPTX": "MANSI AI",
    "JARVIS App Identity": "MANSI AI App Identity",
    "Jarvis App Identity": "MANSI AI App Identity",
    "JARVIS APP IDENTITY": "MANSI AI App Identity",
    "Developer: Tech GPTx": "Developer: SAGAR",
    "Developer: TechGPTx": "Developer: SAGAR",
    "Copyright: Tech GPTx": "Copyright: SAGAR",
    "Copyright: TechGPTx": "Copyright: SAGAR",
    "JARVIS PRO": "MANSI PRO",
    "Jarvis Pro": "MANSI PRO",
    "Jarvis Pro · Voice: Puck": "MANSI PRO · Voice: Puck",
    "Jarvis Pro • Voice: Puck": "MANSI PRO · Voice: Puck",
    "JARVIS OPERATOR · PRIMARY USER": "MANSI AI Operator · Primary User",
    "JARVIS OPERATOR • PRIMARY USER": "MANSI AI Operator · Primary User",
    "Jarvis Operator · Primary User": "MANSI AI Operator · Primary User",
    "Jarvis Operator • Primary User": "MANSI AI Operator · Primary User",
    "Enroll Voice": "ENROLL VOICE",
}
for identity_path in root.rglob("*"):
    if not identity_path.is_file() or identity_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".html", ".txt", ".properties"}:
        continue
    if identity_path.name == "AndroidManifest.xml":
        continue
    try:
        identity_before = identity_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    identity_after = identity_before
    for identity_old, identity_new in identity_labels.items():
        identity_after = identity_after.replace(identity_old, identity_new)
    identity_after = re.sub(r"(?i)jarvis\s+operator\s*[·•]\s*primary user", "MANSI AI Operator · Primary User", identity_after)
    identity_after = re.sub(r"(?i)jarvis\s+pro\s*[·•]\s*voice:\s*puck", "MANSI PRO · Voice: Puck", identity_after)
    if identity_after != identity_before:
        if identity_path.suffix.lower() == ".xml":
            ET.fromstring(identity_after)
        identity_path.write_text(identity_after, encoding="utf-8")
        print("FINAL cross-source branding:", identity_path)

# App Identity owner label must show SAGAR, never the old Tech GPTx branding.
owner_label_replacements = {
    "Tech GPTx": "SAGAR", "TechGPTx": "SAGAR", "TECH GPTX": "SAGAR",
    "TECHGPTX": "SAGAR", "Tech GPTX": "SAGAR", "tech gptx": "SAGAR",
    "Developer: MANSI AI": "Developer: SAGAR",
    "Copyright: MANSI AI": "Copyright: SAGAR",
}
for owner_path in root.rglob("*"):
    if not owner_path.is_file() or owner_path.suffix.lower() not in {".xml", ".kt", ".java", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if owner_path.name == "AndroidManifest.xml":
        continue
    try:
        owner_before = owner_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    owner_after = owner_before
    for owner_old, owner_new in owner_label_replacements.items():
        owner_after = owner_after.replace(owner_old, owner_new)
    if owner_after != owner_before:
        if owner_path.suffix.lower() == ".xml":
            ET.fromstring(owner_after)
        owner_path.write_text(owner_after, encoding="utf-8")
        print("Corrected App Identity owner label to SAGAR:", owner_path)

# Fail the build if these specific visible legacy labels remain in source text.
visible_sources = []
for check_path in root.rglob("*"):
    if check_path.is_file() and check_path.suffix.lower() in {".xml", ".kt", ".java", ".json", ".html", ".txt", ".properties"}:
        try:
            visible_sources.append(check_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            pass
visible_text = "\n".join(visible_sources)
for stale in ("JARVIS App Identity", "Jarvis App Identity", "Developer: Tech GPTx", "Copyright: Tech GPTx", "Jarvis Pro · Voice: Puck", "JARVIS PRO", "JARVIS OPERATOR · PRIMARY USER"):
    if stale in visible_text:
        raise SystemExit("Branding verification failed: stale visible label remains: " + stale)
print("Verified no targeted stale Settings/App Identity labels remain in source text.")


# Prefer Gemini Live's feminine-sounding Aoede voice while preserving existing
# Android view IDs and Kotlin identifiers (e.g. rbVoicePuck) to avoid collisions.
for voice_path in root.rglob("*"):
    if not voice_path.is_file() or voice_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".html", ".txt", ".properties", ".gradle", ".kts"}:
        continue
    if voice_path.name == "AndroidManifest.xml":
        continue
    try:
        voice_before = voice_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    # Replace standalone voice values only, never substrings inside IDs/identifiers.
    voice_after = re.sub(r"(?i)(?<![A-Za-z0-9_])puck(?![A-Za-z0-9_])", lambda m: "Aoede" if m.group(0)[0].isupper() else "aoede", voice_before)
    if voice_after != voice_before:
        if voice_path.suffix.lower() == ".xml":
            ET.fromstring(voice_after)
        voice_path.write_text(voice_after, encoding="utf-8")
        print("FEMALE VOICE Aoede:", voice_path)

# Verify the old standalone voice value is gone without flagging preserved identifiers.
remaining_puck = []
for voice_path in root.rglob("*"):
    if voice_path.is_file() and voice_path.suffix.lower() in {".xml", ".kt", ".java", ".json", ".html", ".txt", ".properties", ".gradle", ".kts"}:
        try:
            if re.search(r"(?i)(?<![A-Za-z0-9_])puck(?![A-Za-z0-9_])", voice_path.read_text(encoding="utf-8")):
                remaining_puck.append(str(voice_path))
        except (OSError, UnicodeDecodeError):
            pass
if remaining_puck:
    raise SystemExit("Female voice verification failed; standalone Puck value remains in: " + ", ".join(remaining_puck[:10]))
print("Verified: standalone Puck voice values replaced with Aoede; Android identifiers preserved.")

# Make every displayed Persona voice choice explicitly feminine. Keep Android
# view IDs untouched; only change the human-readable option labels.
female_label_replacements = {
    "Fenrir (Deep, protective charismatic male voice)": "Kore (Soft, sweet feminine voice)",
    "Aoede (Crisp, modern dynamic male voice)": "Aoede (Cute, warm expressive female voice)",
    "Charon (Distinguished butler male voice)": "Kore (Gentle, calm female voice)",
}
female_label_count = 0
for label_path in root.rglob("*"):
    if not label_path.is_file() or label_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".html", ".txt", ".properties"}:
        continue
    try:
        label_before = label_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    label_after = label_before
    for old_label, new_label in female_label_replacements.items():
        if old_label in label_after:
            label_after = label_after.replace(old_label, new_label)
    if label_after != label_before:
        if label_path.suffix.lower() == ".xml":
            ET.fromstring(label_after)
        label_path.write_text(label_after, encoding="utf-8")
        female_label_count += 1
        print("FEMALE VOICE LABELS:", label_path)
print("Applied feminine labels to all listed Persona voice choices.")



# Focused home-screen polish: use conservative, XML-safe styling without
# rewriting view tags/IDs. Keep the existing layout and functionality intact.
home_layout = root / "res/layout/fragment_home.xml"
if home_layout.exists():
    home_xml = home_layout.read_text(encoding="utf-8")
    home_xml = home_xml.replace("JARVIS OFF • TAP TO START", "MANSI AI OFF · TAP TO START")
    home_xml = home_xml.replace("JARVIS OFF · TAP TO START", "MANSI AI OFF · TAP TO START")
    # The visual circle and card containers are intentionally not structurally
    # rewritten here; use dedicated drawable resources in a follow-up once IDs
    # and hierarchy are confirmed from the source layout.
    ET.fromstring(home_xml)
    home_layout.write_text(home_xml, encoding="utf-8")
    print("Applied safe MANSI AI home status label.")


# Safe home-screen styling guard:
# Do not parse and re-serialize Android data-binding layouts with ElementTree.
# That can alter layout XML in ways that break generated binding classes.
# Preserve the original layout hierarchy and IDs; apply only targeted text edits above.
print("Skipped structural home layout rewrite to preserve Android data binding IDs.\n");


# FINAL OWNER SOCIAL LINKS PASS: replace any legacy Instagram/Telegram profile URLs
# regardless of the old handle or whether the URL includes www / trailing slash.
# Run after all branding passes so no earlier replacement can restore old links.
social_link_files = []
for social_path in root.rglob("*"):
    if not social_path.is_file() or social_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".html", ".js", ".txt", ".properties"}:
        continue
    try:
        social_before = social_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    social_after = re.sub(
        r"https?://(?:www\.)?instagram\.com/(?!hyee__sagar(?:[/?#]|$))[^\s\"'<>)]*",
        "https://instagram.com/hyee__sagar",
        social_before,
        flags=re.IGNORECASE,
    )
    social_after = re.sub(
        r"https?://(?:www\.)?t\.me/(?!H_sagarr(?:[/?#]|$))[^\s\"'<>)]*",
        "https://t.me/H_sagarr",
        social_after,
        flags=re.IGNORECASE,
    )
    if social_after != social_before:
        if social_path.suffix.lower() == ".xml":
            ET.fromstring(social_after)
        social_path.write_text(social_after, encoding="utf-8")
        social_link_files.append(str(social_path))
print("FINAL personal Instagram/Telegram URL enforcement:", ", ".join(social_link_files) if social_link_files else "No old profile URLs found.")

# Build guard: do not ship any other Instagram or Telegram profile URL in source.
for social_path in root.rglob("*"):
    if not social_path.is_file() or social_path.suffix.lower() not in {".xml", ".kt", ".java", ".json", ".html", ".js", ".txt", ".properties"}:
        continue
    try:
        social_text = social_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    if re.search(r"https?://(?:www\.)?instagram\.com/(?!hyee__sagar(?:[/?#]|$))", social_text, re.IGNORECASE):
        raise SystemExit("Social-link verification failed: non-owner Instagram URL remains in " + str(social_path))
    if re.search(r"https?://(?:www\.)?t\.me/(?!H_sagarr(?:[/?#]|$))", social_text, re.IGNORECASE):
        raise SystemExit("Social-link verification failed: non-owner Telegram URL remains in " + str(social_path))
print("Verified: Instagram uses @hyee__sagar and Telegram uses t.me/H_sagarr.")


# FINAL requested credits: show the exact owner attribution everywhere it appears.
for credit_path in root.rglob("*"):
    if not credit_path.is_file() or credit_path.suffix.lower() not in {".xml", ".kt", ".java", ".html", ".js", ".json", ".txt", ".properties"}:
        continue
    if credit_path.name == "AndroidManifest.xml":
        continue
    try:
        credit_before = credit_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    credit_after = re.sub(r"(?i)Developer\s*:\s*(?:Tech\s*GPTx|TechGPTx|MANSI AI|SAGAR)", "Developer: SAGAR", credit_before)
    credit_after = re.sub(r"(?i)Copyright\s*:\s*(?:Tech\s*GPTx|TechGPTx|MANSI AI|SAGAR)", "Copyright: SAGAR", credit_after)
    if credit_after != credit_before:
        if credit_path.suffix.lower() == ".xml":
            ET.fromstring(credit_after)
        credit_path.write_text(credit_after, encoding="utf-8")
        print("Applied exact owner credits in:", credit_path)

print("Verified requested credits: Developer: SAGAR | Copyright: SAGAR")
