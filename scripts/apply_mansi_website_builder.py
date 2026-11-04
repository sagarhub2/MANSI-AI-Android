#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("source/mansi/app/src/main")
PACKAGE = ROOT / "java/com/jarvis/assistant"
ASSETS = ROOT / "assets"
def replace_once(path, old, new, label):
    text = path.read_text(encoding="utf-8")
    if new.strip() in text:
        return text
    if old not in text:
        raise SystemExit(f"Could not find {label} marker in {path}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    return text

activity = PACKAGE / "ui/tools/MansiWebsiteBuilderActivity.kt"
activity.parent.mkdir(parents=True, exist_ok=True)
activity.write_text((Path("scripts/mansi_website_builder/MansiWebsiteBuilderActivity.kt")).read_text(encoding="utf-8"), encoding="utf-8")
layout = ROOT / "res/layout/activity_mansi_website_builder.xml"
layout.parent.mkdir(parents=True, exist_ok=True)
layout.write_text((Path("scripts/mansi_website_builder/activity_mansi_website_builder.xml")).read_text(encoding="utf-8"), encoding="utf-8")
ASSETS.mkdir(parents=True, exist_ok=True)
(ASSETS / "mansi-website-builder.html").write_text((Path("scripts/mansi_website_builder/mansi-website-builder.html")).read_text(encoding="utf-8"), encoding="utf-8")

manifest_path = ROOT / "AndroidManifest.xml"
manifest = manifest_path.read_text(encoding="utf-8")
if ".ui.tools.MansiWebsiteBuilderActivity" not in manifest:
    marker = '        <activity\n            android:name=".ui.settings.SettingsActivity"'
    declaration = '''        <activity
            android:name=".ui.tools.MansiWebsiteBuilderActivity"
            android:exported="false"
            android:screenOrientation="portrait"
            android:windowSoftInputMode="adjustResize" />

'''
    manifest = replace_once(manifest_path, marker, declaration + marker, "SettingsActivity")
    ET.parse(manifest_path)

settings_layout_path = ROOT / "res/layout/fragment_settings.xml"
layout_text = settings_layout_path.read_text(encoding="utf-8")
if "rowMansiWebsiteBuilder" not in layout_text:
    marker = '            <LinearLayout\n                android:id="@+id/rowMansiGuard"'
    row = '''            <LinearLayout
                android:id="@+id/rowMansiWebsiteBuilder"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:background="@drawable/bg_jarvis_card"
                android:padding="16dp"
                android:layout_marginBottom="12dp"
                android:clickable="true"
                android:focusable="true">
                <FrameLayout
                    android:layout_width="44dp"
                    android:layout_height="44dp"
                    android:background="@drawable/bg_jarvis_icon_square">
                    <ImageView
                        android:layout_width="24dp"
                        android:layout_height="24dp"
                        android:layout_gravity="center"
                        android:src="@drawable/ic_settings_shield"
                        app:tint="#8D83FF"
                        android:contentDescription="Website Builder" />
                </FrameLayout>
                <LinearLayout
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:orientation="vertical"
                    android:layout_marginStart="14dp">
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="MANSI WEBSITE BUILDER"
                        android:textColor="?attr/themeTextPrimary"
                        android:textSize="15sp"
                        android:textStyle="bold" />
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Create, preview, edit &amp; export websites"
                        android:textColor="?attr/themeTextMuted"
                        android:textSize="12sp"
                        android:layout_marginTop="3dp" />
                </LinearLayout>
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="›"
                    android:textColor="?attr/themeAccent"
                    android:textSize="26sp" />
            </LinearLayout>

'''
    layout_text = replace_once(settings_layout_path, marker, row + marker, "MANSI GUARD settings row")
    ET.parse(settings_layout_path)

fragment_path = PACKAGE / "ui/settings/SettingsFragment.kt"
fragment = fragment_path.read_text(encoding="utf-8")
if "import com.jarvis.assistant.ui.tools.MansiWebsiteBuilderActivity" not in fragment:
    marker = "import com.jarvis.assistant.ui.security.MansiGuardActivity"
    fragment = replace_once(fragment_path, marker, marker + "\nimport com.jarvis.assistant.ui.tools.MansiWebsiteBuilderActivity", "MANSI GUARD import")
if "binding.rowMansiWebsiteBuilder.setOnClickListener" not in fragment:
    marker = "        // MANSI GUARD — Advanced Alert Mode"
    listener = '''        // MANSI Website Builder — prompt, preview, edit and export
        binding.rowMansiWebsiteBuilder.setOnClickListener {
            startActivity(Intent(requireContext(), MansiWebsiteBuilderActivity::class.java))
        }

'''
    replace_once(fragment_path, marker, listener + marker, "MANSI GUARD click listener")

ET.parse(manifest_path)
ET.parse(settings_layout_path)
assert (ASSETS / "mansi-website-builder.html").is_file()
assert "rowMansiWebsiteBuilder" in settings_layout_path.read_text(encoding="utf-8")
assert "MansiWebsiteBuilderActivity" in manifest_path.read_text(encoding="utf-8")
print("MANSI Website Builder applied: Settings entry, WebView workspace, prompt starter templates, live preview, HTML editor and native HTML export.")
