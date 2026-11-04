#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("source/mansi/app/src/main")
PACKAGE = ROOT / "java/com/jarvis/assistant"
activity_src = Path("scripts/mansi_icon_studio/MansiIconStudioActivity.kt")
activity_dst = PACKAGE / "ui/tools/MansiIconStudioActivity.kt"
activity_dst.parent.mkdir(parents=True, exist_ok=True)
activity_dst.write_text(activity_src.read_text(encoding="utf-8"), encoding="utf-8")

manifest_path = ROOT / "AndroidManifest.xml"
manifest = manifest_path.read_text(encoding="utf-8")
if ".ui.tools.MansiIconStudioActivity" not in manifest:
    marker = '        <activity\n            android:name=".ui.settings.SettingsActivity"'
    declaration = '''        <activity
            android:name=".ui.tools.MansiIconStudioActivity"
            android:exported="false"
            android:screenOrientation="portrait" />

'''
    if marker not in manifest:
        raise SystemExit("Could not find SettingsActivity manifest marker")
    manifest = manifest.replace(marker, declaration + marker, 1)
    manifest_path.write_text(manifest, encoding="utf-8")
ET.parse(manifest_path)

settings_path = PACKAGE / "ui/settings/SettingsFragment.kt"
settings = settings_path.read_text(encoding="utf-8")
imp = "import com.jarvis.assistant.ui.tools.MansiIconStudioActivity"
if imp not in settings:
    marker = "import com.jarvis.assistant.ui.security.MansiGuardActivity"
    if marker not in settings:
        raise SystemExit("Could not find MANSI GUARD import marker")
    settings = settings.replace(marker, marker + "\n" + imp, 1)
listener = '''        // MANSI Icon Studio — create, preview, save and pin a custom home icon
        binding.rowMansiIconStudio.setOnClickListener {
            startActivity(Intent(requireContext(), MansiIconStudioActivity::class.java))
        }

'''
if "binding.rowMansiIconStudio.setOnClickListener" not in settings:
    marker = "        // MANSI GUARD — Advanced Alert Mode"
    if marker not in settings:
        raise SystemExit("Could not find MANSI GUARD listener marker")
    settings = settings.replace(marker, listener + marker, 1)
settings_path.write_text(settings, encoding="utf-8")

layout_path = ROOT / "res/layout/fragment_settings.xml"
layout = layout_path.read_text(encoding="utf-8")
if "rowMansiIconStudio" not in layout:
    marker = '            <LinearLayout\n                android:id="@+id/rowMansiGuard"'
    row = '''            <LinearLayout
                android:id="@+id/rowMansiIconStudio"
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
                    <TextView
                        android:layout_width="match_parent"
                        android:layout_height="match_parent"
                        android:gravity="center"
                        android:text="🎨"
                        android:textSize="22sp"
                        android:contentDescription="Icon Studio" />
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
                        android:text="MANSI ICON STUDIO"
                        android:textColor="?attr/themeTextPrimary"
                        android:textSize="15sp"
                        android:textStyle="bold" />
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Custom icon, gallery, gradients &amp; preview"
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
    if marker not in layout:
        raise SystemExit("Could not find MANSI GUARD settings row marker")
    layout = layout.replace(marker, row + marker, 1)
    layout_path.write_text(layout, encoding="utf-8")
ET.parse(layout_path)
print("MANSI Icon Studio applied: gallery image, gradient presets, live preview, PNG export and custom pinned home-screen shortcut.")
