#!/usr/bin/env python3
"""Wire AudioPlayer RMS amplitude into the MANSI anime avatar WebView."""
from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
audio = ROOT / "java/com/jarvis/assistant/audio/AudioPlayer.kt"
home = ROOT / "java/com/jarvis/assistant/ui/home/HomeFragment.kt"
bridge = ROOT / "java/com/jarvis/assistant/ui/home/MansiAvatarAudioBridge.kt"
orb = ROOT / "assets/orb.html"

for required in (audio, home, orb):
    if not required.is_file():
        raise SystemExit(f"Required source file missing: {required}")

# AudioPlayer already calculates normalized RMS amplitude. Forward each real
# playback chunk (and the zero level emitted at playback end) to the WebView.
audio_text = audio.read_text(encoding="utf-8")
audio_text, amplitude_count = re.subn(
    r"(?m)^(\s*)onPlaybackAmplitude\((amplitude|0f)\)\s*$",
    lambda m: (
        m.group(1) + f"onPlaybackAmplitude({m.group(2)})\n" +
        m.group(1) + f"com.jarvis.assistant.ui.home.MansiAvatarAudioBridge.onAmplitude({m.group(2)})"
    ),
    audio_text,
)
if amplitude_count < 2:
    if "MansiAvatarAudioBridge.onAmplitude" not in audio_text:
        raise SystemExit(f"Expected AudioPlayer amplitude callbacks; patched {amplitude_count} only.")
audio.write_text(audio_text, encoding="utf-8")
print(f"Connected {amplitude_count} AudioPlayer RMS callback sites to the avatar bridge.")

# Attach the current HomeFragment WebView to a weak-reference bridge.
home_text = home.read_text(encoding="utf-8")
anchor = "private fun setupOrbWebView() {"
if "MansiAvatarAudioBridge.attach(binding.orbWebView)" not in home_text:
    if anchor not in home_text:
        raise SystemExit("Could not find HomeFragment.setupOrbWebView() safely.")
    home_text = home_text.replace(
        anchor,
        anchor + "\n        MansiAvatarAudioBridge.attach(binding.orbWebView)",
        1,
    )
    home.write_text(home_text, encoding="utf-8")
    print("Attached the home orb WebView to the audio bridge.")
else:
    print("Home orb WebView bridge attachment already exists.")

bridge.parent.mkdir(parents=True, exist_ok=True)
bridge.write_text("""package com.jarvis.assistant.ui.home

import android.webkit.WebView
import java.lang.ref.WeakReference
import java.util.Locale

/**
 * Delivers real AudioPlayer RMS levels to the currently visible MANSI avatar.
 * AudioPlayer calls this from its playback worker; WebView work is posted to UI.
 */
object MansiAvatarAudioBridge {
    @Volatile
    private var webViewRef: WeakReference<WebView>? = null

    fun attach(webView: WebView) {
        webViewRef = WeakReference(webView)
    }

    fun onAmplitude(amplitude: Float) {
        val webView = webViewRef?.get() ?: return
        val level = amplitude.coerceIn(0f, 1f)
        val jsLevel = String.format(Locale.US, "%.4f", level)
        webView.post {
            if (webView.isAttachedToWindow) {
                webView.evaluateJavascript(
                    "window.MANSIAvatarAudioLevel && window.MANSIAvatarAudioLevel($jsLevel);",
                    null
                )
            }
        }
    }
}
""", encoding="utf-8")
print("Created MansiAvatarAudioBridge.kt.")

# Close the mouth when AudioPlayer reports silence/end-of-playback.
html = orb.read_text(encoding="utf-8")
old = "if(value>.025) orb.classList.add('speaking');"
new = "if(value>.025) orb.classList.add('speaking'); else if(!orb.classList.contains('listening')) orb.classList.remove('speaking');"
if old in html:
    html = html.replace(old, new, 1)
elif new not in html:
    raise SystemExit("Could not find the expected MANSIAvatarAudioLevel() hook in orb.html.")
orb.write_text(html, encoding="utf-8")
print("Connected avatar mouth opening/closing to live RMS levels.")
