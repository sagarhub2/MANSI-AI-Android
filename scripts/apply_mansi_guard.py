#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("source/mansi/app/src/main")
REPO = Path("scripts/mansi_guard")
PACKAGE = Path("source/mansi/app/src/main/java/com/jarvis/assistant")

def copy(src: str, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes((REPO / src).read_bytes())

copy("MansiGuardActivity.kt", PACKAGE / "ui/security/MansiGuardActivity.kt")
copy("MansiGuardService.kt", PACKAGE / "background/MansiGuardService.kt")
copy("activity_mansi_guard.xml", ROOT / "res/layout/activity_mansi_guard.xml")

manifest_path = ROOT / "AndroidManifest.xml"
manifest = manifest_path.read_text(encoding="utf-8")
if "android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" not in manifest:
    manifest = manifest.replace(
        '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />',
        '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />\n'
        '    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />'
    )
if 'android.permission.VIBRATE' not in manifest:
    manifest = manifest.replace('<application', '<uses-permission android:name="android.permission.VIBRATE" />\n\n    <application', 1)
if '.ui.security.MansiGuardActivity' not in manifest:
    marker = '        <activity\n            android:name=".ui.settings.SettingsActivity"'
    activity = '''        <activity
            android:name=".ui.security.MansiGuardActivity"
            android:exported="false"
            android:screenOrientation="portrait"
            android:windowSoftInputMode="adjustResize" />

'''
    if marker not in manifest:
        raise SystemExit("Could not find SettingsActivity marker in AndroidManifest.xml")
    manifest = manifest.replace(marker, activity + marker, 1)
if '.background.MansiGuardService' not in manifest:
    marker = '        <service\n            android:name=".background.JarvisConversationService"'
    service = '''        <service
            android:name=".background.MansiGuardService"
            android:exported="false"
            android:stopWithTask="false"
            android:foregroundServiceType="mediaPlayback" />

'''
    if marker not in manifest:
        raise SystemExit("Could not find JarvisConversationService marker in AndroidManifest.xml")
    manifest = manifest.replace(marker, service + marker, 1)
manifest_path.write_text(manifest, encoding="utf-8")

settings_layout_path = ROOT / "res/layout/fragment_settings.xml"
layout = settings_layout_path.read_text(encoding="utf-8")
if "rowMansiGuard" not in layout:
    marker = "            <!-- Social Community Buttons -->"
    row = '''            <!-- MANSI GUARD: Advanced Anti-Theft Alert Mode -->
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="SECURITY &amp; PROTECTION"
                android:textColor="?attr/themeTextMuted"
                android:textSize="11sp"
                android:letterSpacing="0.08"
                android:fontFamily="sans-serif-medium"
                android:textStyle="bold"
                android:layout_marginTop="8dp"
                android:layout_marginBottom="8dp" />

            <LinearLayout
                android:id="@+id/rowMansiGuard"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:background="@drawable/bg_jarvis_card"
                android:padding="16dp"
                android:layout_marginBottom="20dp"
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
                        app:tint="#FF6C9F"
                        android:contentDescription="MANSI Guard" />
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
                        android:text="MANSI GUARD"
                        android:textColor="?attr/themeTextPrimary"
                        android:textSize="15sp"
                        android:textStyle="bold" />
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Advanced anti-theft alerts &amp; PIN protection"
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
        raise SystemExit("Could not find Social Community Buttons marker in fragment_settings.xml")
    layout = layout.replace(marker, row + marker, 1)
    settings_layout_path.write_text(layout, encoding="utf-8")

fragment_path = PACKAGE / "ui/settings/SettingsFragment.kt"
fragment = fragment_path.read_text(encoding="utf-8")
if "import com.jarvis.assistant.ui.security.MansiGuardActivity" not in fragment:
    marker = "import com.jarvis.assistant.ui.voice.VoiceEnrollmentActivity"
    if marker not in fragment:
        raise SystemExit("Could not find VoiceEnrollmentActivity import in SettingsFragment.kt")
    fragment = fragment.replace(marker, marker + "\nimport com.jarvis.assistant.ui.security.MansiGuardActivity", 1)
if "binding.rowMansiGuard.setOnClickListener" not in fragment:
    marker = "        // Social Media Community Buttons"
    listener = '''        // MANSI GUARD — Advanced Alert Mode
        binding.rowMansiGuard.setOnClickListener {
            startActivity(Intent(requireContext(), MansiGuardActivity::class.java))
        }

'''
    if marker not in fragment:
        raise SystemExit("Could not find Social Media Community Buttons listener marker")
    fragment = fragment.replace(marker, listener + marker, 1)
    fragment_path.write_text(fragment, encoding="utf-8")

# Fail fast on malformed XML before Gradle starts.
ET.parse(manifest_path)
ET.parse(settings_layout_path)
ET.parse(ROOT / "res/layout/activity_mansi_guard.xml")
assert "rowMansiGuard" in settings_layout_path.read_text(encoding="utf-8")
assert "MansiGuardService" in manifest_path.read_text(encoding="utf-8")
print("MANSI GUARD applied: Activity, settings entry, foreground service, movement/screen-wake/charger alerts, PIN disarm.")
