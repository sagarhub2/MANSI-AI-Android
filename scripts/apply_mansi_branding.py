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
        'binding.btnSocialTelegram.setOnClickListener {\\n            openUrl("https://t.me/H_sagarr")\\n        }',
        src, count=1, flags=re.S
    )
    # Hide the old YouTube profile shortcut; leave YouTube automation features untouched.
    if "binding.btnSocialYoutube.visibility = View.GONE" not in src:
        src = src.replace(
            "binding.btnSocialYoutube.setOnClickListener {",
            "binding.btnSocialYoutube.visibility = View.GONE\\n        binding.btnSocialYoutube.setOnClickListener {",
            1
        )
    settings_kt.write_text(src, encoding="utf-8")

privacy_kt = root / "java/com/jarvis/assistant/ui/settings/PrivacyShieldActivity.kt"
if privacy_kt.exists():
    src = privacy_kt.read_text(encoding="utf-8")
    src = src.replace("https://www.instagram.com/techgptx.ai", "https://instagram.com/hyee__sagar")
    src = re.sub(
        r'binding\.btnJoinOfficialTelegram\.setOnClickListener \{.*?\n        \}',
        'binding.btnJoinOfficialTelegram.setOnClickListener {\\n            openUrl("https://t.me/H_sagarr")\\n        }',
        src, count=1, flags=re.S
    )
    src = re.sub(
        r'binding\.btnJoinTelegram\.setOnClickListener \{.*?\n        \}',
        'binding.btnJoinTelegram.setOnClickListener {\\n            openUrl("https://t.me/H_sagarr")\\n        }',
        src, count=1, flags=re.S
    )
    if "binding.btnJoinYoutube.visibility = View.GONE" not in src:
        src = src.replace(
            "binding.btnJoinYoutube.setOnClickListener {",
            "binding.btnJoinYoutube.visibility = View.GONE\\n        binding.btnJoinYoutube.setOnClickListener {",
            1
        )
    privacy_kt.write_text(src, encoding="utf-8")
print("Applied personal Instagram/Telegram links and hid old YouTube profile shortcuts.")
