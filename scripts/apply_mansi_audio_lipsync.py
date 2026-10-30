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


# Add touch-follow 3D parallax and state-linked expressive transitions.
# This runs after the anime avatar is installed and does not replace its heart/orb.
html = orb.read_text(encoding="utf-8")
motion_marker = "MANSI_ANIME_3D_MOTION_V1"
if motion_marker not in html:
    motion_patch = r"""
<style>
/* MANSI_ANIME_3D_MOTION_V1 */
#mansi-final-orb { perspective:900px; transform-style:preserve-3d; }
#mansi-final-orb .mansi-anime-avatar.mansi-3d {
  transform-style:preserve-3d;
  will-change:filter;
}
#mansi-final-orb .mansi-anime-art {
  transform-origin:50% 48%;
  transform:translate3d(var(--mansi-face-shift-x,0px),var(--mansi-face-shift-y,0px),0)
    rotateX(var(--mansi-face-tilt-y,0deg)) rotateY(var(--mansi-face-tilt-x,0deg)) scale(1.025);
  transition:filter .22s ease, transform .16s ease-out;
  backface-visibility:hidden;
}
#mansi-final-orb .mansi-anime-avatar.mansi-curious {
  filter:drop-shadow(0 9px 16px rgba(91,196,255,.38)) saturate(1.08);
}
#mansi-final-orb .mansi-anime-avatar.mansi-excited {
  filter:drop-shadow(0 0 15px rgba(255,112,218,.58)) saturate(1.15) brightness(1.04);
}
#mansi-final-orb .mansi-eye-glint {
  transition:transform .12s ease-out, opacity .2s ease;
}
@media (prefers-reduced-motion:reduce) {
  #mansi-final-orb .mansi-anime-art { transition:none!important; transform:none!important; }
}
</style>
<script>
(function(){
  const orb=document.getElementById('mansi-final-orb');
  if(!orb || orb.dataset.mansi3dMotion==='1') return;
  const face=orb.querySelector('.mansi-anime-avatar.mansi-3d');
  const art=face && face.querySelector('.mansi-anime-art');
  if(!face || !art) return;
  orb.dataset.mansi3dMotion='1';
  let lastX=0,lastY=0;
  function setPose(clientX,clientY){
    const rect=orb.getBoundingClientRect();
    if(!rect.width || !rect.height) return;
    const nx=Math.max(-1,Math.min(1,((clientX-rect.left)/rect.width-.5)*2));
    const ny=Math.max(-1,Math.min(1,((clientY-rect.top)/rect.height-.5)*2));
    lastX=nx;lastY=ny;
    art.style.setProperty('--mansi-face-shift-x',(nx*2.4).toFixed(2)+'px');
    art.style.setProperty('--mansi-face-shift-y',(ny*1.8).toFixed(2)+'px');
    art.style.setProperty('--mansi-face-tilt-x',(nx*5.5).toFixed(2)+'deg');
    art.style.setProperty('--mansi-face-tilt-y',(-ny*4.5).toFixed(2)+'deg');
    face.querySelectorAll('.mansi-eye-glint').forEach((eye,i)=>{
      eye.style.transform='translate('+(nx*2.1)+'px,'+(ny*1.5)+'px)';
    });
  }
  function resetPose(){
    art.style.setProperty('--mansi-face-shift-x','0px');
    art.style.setProperty('--mansi-face-shift-y','0px');
    art.style.setProperty('--mansi-face-tilt-x','0deg');
    art.style.setProperty('--mansi-face-tilt-y','0deg');
    face.querySelectorAll('.mansi-eye-glint').forEach(eye=>eye.style.transform='translate(0,0)');
  }
  orb.addEventListener('pointermove',e=>setPose(e.clientX,e.clientY),{passive:true});
  orb.addEventListener('pointerleave',resetPose,{passive:true});
  orb.addEventListener('pointercancel',resetPose,{passive:true});
  function syncExpression(){
    face.classList.toggle('mansi-curious',orb.classList.contains('listening'));
    face.classList.toggle('mansi-excited',orb.classList.contains('speaking'));
  }
  new MutationObserver(syncExpression).observe(orb,{attributes:true,attributeFilter:['class']});
  syncExpression();
  // On touch devices, keep the avatar responsive to a finger moving over the orb.
  orb.addEventListener('touchmove',e=>{
    if(!e.touches || !e.touches.length) return;
    setPose(e.touches[0].clientX,e.touches[0].clientY);
  },{passive:true});
  orb.addEventListener('touchend',resetPose,{passive:true});
})();
</script>
"""
    if re.search(r"</body\s*>", html, re.I):
        html = re.sub(r"</body\\s*>", motion_patch + "\n</body>", html, count=1, flags=re.I)
    else:
        html += "\n" + motion_patch
    orb.write_text(html, encoding="utf-8")
    print("Added touch-follow 3D parallax, eye tracking and listening/speaking expression transitions.")
else:
    print("MANSI 3D avatar motion already installed.")
