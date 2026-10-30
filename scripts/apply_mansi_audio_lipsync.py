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
    body_close = html.lower().rfind("</body>")
    if body_close >= 0:
        html = html[:body_close] + motion_patch + "\\n" + html[body_close:]
    else:
        html += "\\n" + motion_patch
    orb.write_text(html, encoding="utf-8")
    print("Added touch-follow 3D parallax, eye tracking and listening/speaking expression transitions.")
else:
    print("MANSI 3D avatar motion already installed.")


# Expose stable mood and palette controls for future in-app customization.
html = orb.read_text(encoding="utf-8")
api_marker = "MANSI_AVATAR_CUSTOMIZATION_API_V1"
if api_marker not in html:
    api_script = r"""
<script>
/* MANSI_AVATAR_CUSTOMIZATION_API_V1 */
(function(){
  function install(){
    const orb=document.getElementById('mansi-final-orb');
    const face=orb && orb.querySelector('.mansi-anime-avatar');
    if(!orb || !face) return false;
    window.MANSIAvatarSetMood=function(mood){
      const classes=['mansi-happy','mansi-shy','mansi-surprised','mansi-sleepy'];
      face.classList.remove(...classes);
      const map={happy:'mansi-happy',shy:'mansi-shy',surprised:'mansi-surprised',sleepy:'mansi-sleepy',neutral:null};
      const key=String(mood||'neutral').toLowerCase();
      if(!(key in map)) return false;
      if(map[key]) face.classList.add(map[key]);
      return true;
    };
    window.MANSIAvatarSetTheme=function(theme){
      const palettes={pink:['#ff72d2','#c85bff'],purple:['#bd91ff','#755bff'],blue:['#73e6ff','#6887ff']};
      const pair=palettes[String(theme||'pink').toLowerCase()];
      if(!pair) return false;
      face.style.setProperty('--mansi-avatar-accent',pair[0]);
      face.style.filter='drop-shadow(0 8px 15px '+pair[1]+'66) drop-shadow(0 0 10px '+pair[0]+'55)';
      return true;
    };
    return true;
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  new MutationObserver(install).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>
"""
    body_close=html.lower().rfind("</body>")
    if body_close >= 0: html=html[:body_close]+api_script+"\\n"+html[body_close:]
    else: html += "\\n"+api_script
    orb.write_text(html,encoding="utf-8")
    print("Added public mood and pink/purple/blue theme customization hooks.")
else:
    print("MANSI avatar customization API already installed.")


# Install a compact, real in-app avatar customizer in the orb WebView.
html = orb.read_text(encoding="utf-8")
panel_marker = "MANSI_AVATAR_CUSTOMIZER_PANEL_V1"
if panel_marker not in html:
    panel_script = r"""
<style>
/* MANSI_AVATAR_CUSTOMIZER_PANEL_V1 */
#mansi-avatar-customizer{position:fixed;z-index:2147483000;top:max(12px,env(safe-area-inset-top));right:max(12px,env(safe-area-inset-right));font:500 13px/1.35 system-ui,-apple-system,sans-serif;color:#fff}
#mansi-avatar-customizer *{box-sizing:border-box}
#mansi-avatar-customizer .mansi-customizer-trigger{width:42px;height:42px;border:1px solid rgba(255,255,255,.32);border-radius:50%;background:linear-gradient(145deg,rgba(87,72,151,.94),rgba(33,39,79,.94));color:#fff;font-size:19px;box-shadow:0 4px 18px rgba(120,91,255,.38);backdrop-filter:blur(12px)}
#mansi-avatar-customizer .mansi-customizer-panel{display:none;position:absolute;right:0;top:50px;width:min(246px,calc(100vw - 28px));padding:14px;border:1px solid rgba(224,204,255,.28);border-radius:18px;background:linear-gradient(150deg,rgba(38,31,68,.97),rgba(18,23,49,.97));box-shadow:0 12px 34px rgba(0,0,0,.35);backdrop-filter:blur(18px)}
#mansi-avatar-customizer.open .mansi-customizer-panel{display:block;animation:mansi-panel-in .18s ease-out}
#mansi-avatar-customizer .mansi-customizer-title{font-weight:750;font-size:14px;letter-spacing:.2px;margin:0 0 10px}
#mansi-avatar-customizer .mansi-customizer-label{font-size:11px;opacity:.75;margin:12px 0 7px}
#mansi-avatar-customizer .mansi-customizer-row{display:flex;gap:7px;flex-wrap:wrap}
#mansi-avatar-customizer button[data-mansi-choice]{border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:7px 10px;background:rgba(255,255,255,.08);color:#fff;font:600 12px system-ui;min-height:32px}
#mansi-avatar-customizer button[data-mansi-choice][aria-pressed="true"]{border-color:#ff9bdf;background:rgba(255,125,218,.22);box-shadow:0 0 0 1px rgba(255,155,223,.2) inset}
#mansi-avatar-customizer .mansi-customizer-footer{display:flex;justify-content:space-between;align-items:center;margin-top:12px}
#mansi-avatar-customizer .mansi-customizer-reset{border:0;background:none;color:#d9c7ff;text-decoration:underline;padding:4px;font:500 11px system-ui}
@keyframes mansi-panel-in{from{opacity:0;transform:translateY(-5px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}
@media(prefers-reduced-motion:reduce){#mansi-avatar-customizer .mansi-customizer-panel{animation:none}}
</style>
<script>
(function(){
  if(window.__MANSI_CUSTOMIZER_PANEL__) return;
  window.__MANSI_CUSTOMIZER_PANEL__=true;
  function mount(){
    if(!document.body || document.getElementById('mansi-avatar-customizer')) return;
    const root=document.createElement('div');
    root.id='mansi-avatar-customizer';
    root.innerHTML=
      '<button class="mansi-customizer-trigger" type="button" aria-label="Customize MANSI avatar" aria-expanded="false">🎨</button>'+
      '<section class="mansi-customizer-panel" aria-label="Avatar customization">'+
        '<p class="mansi-customizer-title">MANSI look & mood ✨</p>'+
        '<div class="mansi-customizer-label">MOOD</div>'+
        '<div class="mansi-customizer-row" data-group="mood">'+
          '<button type="button" data-mansi-choice="happy">😊 Happy</button>'+
          '<button type="button" data-mansi-choice="shy">🥹 Shy</button>'+
          '<button type="button" data-mansi-choice="surprised">😮 Wow</button>'+
          '<button type="button" data-mansi-choice="sleepy">😴 Sleepy</button>'+
          '<button type="button" data-mansi-choice="neutral">🤍 Calm</button>'+
        '</div>'+
        '<div class="mansi-customizer-label">GLOW COLOR</div>'+
        '<div class="mansi-customizer-row" data-group="theme">'+
          '<button type="button" data-mansi-choice="pink">🩷 Pink</button>'+
          '<button type="button" data-mansi-choice="purple">💜 Purple</button>'+
          '<button type="button" data-mansi-choice="blue">💙 Blue</button>'+
        '</div>'+
        '<div class="mansi-customizer-footer"><span>Saved on this device</span><button class="mansi-customizer-reset" type="button">Reset look</button></div>'+
      '</section>';
    document.body.appendChild(root);
    const trigger=root.querySelector('.mansi-customizer-trigger');
    const panel=root.querySelector('.mansi-customizer-panel');
    const defaults={mood:'happy',theme:'pink'};
    let state={...defaults};
    try{state={...state,...JSON.parse(localStorage.getItem('mansiAvatarLook')||'{}')};}catch(e){}
    function apply(group,value){
      if(group==='mood' && window.MANSIAvatarSetMood(value)) state.mood=value;
      if(group==='theme' && window.MANSIAvatarSetTheme(value)) state.theme=value;
      root.querySelectorAll('[data-group="'+group+'"] [data-mansi-choice]').forEach(b=>{
        b.setAttribute('aria-pressed',String(b.dataset.mansiChoice===value));
      });
      try{localStorage.setItem('mansiAvatarLook',JSON.stringify(state));}catch(e){}
    }
    function restore(){
      if(typeof window.MANSIAvatarSetMood!=='function'||typeof window.MANSIAvatarSetTheme!=='function') return false;
      apply('mood',state.mood);apply('theme',state.theme);return true;
    }
    trigger.addEventListener('click',e=>{
      e.stopPropagation();
      const open=root.classList.toggle('open');
      trigger.setAttribute('aria-expanded',String(open));
    });
    panel.addEventListener('click',e=>{
      e.stopPropagation();
      const choice=e.target.closest('[data-mansi-choice]');
      if(choice){
        const group=choice.closest('[data-group]').dataset.group;
        apply(group,choice.dataset.mansiChoice);
      }
      if(e.target.closest('.mansi-customizer-reset')){
        state={...defaults};restore();
      }
    });
    document.addEventListener('click',e=>{
      if(!root.contains(e.target)){root.classList.remove('open');trigger.setAttribute('aria-expanded','false');}
    });
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'){root.classList.remove('open');trigger.setAttribute('aria-expanded','false');}
    });
    if(!restore()){
      const retry=new MutationObserver(()=>{if(restore())retry.disconnect();});
      retry.observe(document.documentElement,{childList:true,subtree:true});
      setTimeout(()=>retry.disconnect(),8000);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount,{once:true});
  else mount();
})();
</script>
"""
    body_close=html.lower().rfind("</body>")
    if body_close >= 0: html=html[:body_close]+panel_script+"\n"+html[body_close:]
    else: html += "\n"+panel_script
    orb.write_text(html,encoding="utf-8")
    print("Installed persistent in-app MANSI avatar mood and glow customizer.")
else:
    print("MANSI avatar customizer panel already installed.")


# MANSI_AUDIO_REACTIVE_HOLOGRAM_V1: pulse the existing hologram from real TTS RMS.
html = orb.read_text(encoding="utf-8")
audio_visual_marker = "MANSI_AUDIO_REACTIVE_HOLOGRAM_V1"
if audio_visual_marker not in html:
    visual_patch = r"""
<style>
/* MANSI_AUDIO_REACTIVE_HOLOGRAM_V1 */
#mansi-final-orb .mansi-core {
  transition:transform .07s linear,filter .08s linear,box-shadow .08s linear;
  transform:scale(var(--mansi-audio-scale,1));
  filter:brightness(var(--mansi-audio-brightness,1));
  box-shadow:0 0 calc(8px + var(--mansi-audio-glow,0px)) rgba(115,203,255,.34),
             0 0 calc(12px + var(--mansi-audio-pink,0px)) rgba(255,105,215,.28);
}
#mansi-final-orb .mansi-heart {
  transform:translate(-50%,-50%) scale(var(--mansi-heart-pulse,1));
  transition:transform .08s linear,filter .08s linear;
  filter:drop-shadow(0 0 calc(4px + var(--mansi-audio-pink,0px)) #ff65d9)
         drop-shadow(0 0 12px rgba(255,72,216,.72));
}
@media(prefers-reduced-motion:reduce){
  #mansi-final-orb .mansi-core,#mansi-final-orb .mansi-heart{transition:none!important}
}
</style>
<script>
(function(){
  if(window.__MANSI_AUDIO_VISUALIZER_V1) return;
  window.__MANSI_AUDIO_VISUALIZER_V1=true;
  function attach(){
    const orb=document.getElementById('mansi-final-orb');
    if(!orb || typeof window.MANSIAvatarAudioLevel!=='function') return false;
    if(orb.dataset.mansiAudioVisual==='1') return true;
    orb.dataset.mansiAudioVisual='1';
    const original=window.MANSIAvatarAudioLevel;
    let smooth=0;
    window.MANSIAvatarAudioLevel=function(level){
      const value=Math.max(0,Math.min(1,Number(level)||0));
      smooth=smooth*.58+value*.42;
      const glow=(smooth*22).toFixed(1)+'px';
      orb.style.setProperty('--mansi-audio-glow',glow);
      orb.style.setProperty('--mansi-audio-pink',(smooth*16).toFixed(1)+'px');
      orb.style.setProperty('--mansi-audio-scale',(1+smooth*.13).toFixed(3));
      orb.style.setProperty('--mansi-audio-brightness',(1+smooth*.22).toFixed(3));
      orb.style.setProperty('--mansi-heart-pulse',(1+smooth*.24).toFixed(3));
      return original.apply(this,arguments);
    };
    return true;
  }
  if(!attach()){
    const observer=new MutationObserver(()=>{if(attach())observer.disconnect();});
    observer.observe(document.documentElement,{childList:true,subtree:true});
    setTimeout(()=>observer.disconnect(),10000);
  }
})();
</script>
"""
    body_close=html.lower().rfind("</body>")
    if body_close >= 0: html=html[:body_close]+visual_patch+"\n"+html[body_close:]
    else: html += "\n"+visual_patch
    orb.write_text(html,encoding="utf-8")
    print("Added RMS-reactive hologram glow and pink heart pulse.")
else:
    print("Audio-reactive hologram visualizer already installed.")


# MANSI_GLOW_SENSITIVITY_V1
# Let users tune how strongly the hologram and pink heart react to MANSI's voice.
html = orb.read_text(encoding="utf-8")
if "MANSI_GLOW_SENSITIVITY_V1" not in html:
    html = html.replace(
        "smooth=smooth*.58+value*.42;",
        "const sensitivity=Math.max(.35,Math.min(2,Number(window.MANSIAvatarGlowSensitivity)||1));\\n      smooth=smooth*.58+Math.min(1,value*sensitivity)*.42;"
    )
    sensitivity_ui = r"""
<style>
/* MANSI_GLOW_SENSITIVITY_V1 */
#mansi-avatar-customizer .mansi-glow-control{margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,.12)}
#mansi-avatar-customizer .mansi-glow-control label{display:flex;justify-content:space-between;font-size:11px;opacity:.85;margin-bottom:6px}
#mansi-avatar-customizer .mansi-glow-control input{width:100%;accent-color:#ff8bdc}
</style>
<script>
(function(){
  function mountSensitivity(){
    const panel=document.querySelector('#mansi-avatar-customizer .mansi-customizer-panel');
    if(!panel || panel.querySelector('.mansi-glow-control')) return !!panel;
    const control=document.createElement('div');
    control.className='mansi-glow-control';
    control.innerHTML='<label for="mansi-glow-sensitivity"><span>VOICE GLOW INTENSITY</span><span id="mansi-glow-value">100%</span></label><input id="mansi-glow-sensitivity" type="range" min="35" max="200" step="5" value="100">';
    const footer=panel.querySelector('.mansi-customizer-footer');
    panel.insertBefore(control,footer||null);
    const slider=control.querySelector('input');
    const output=control.querySelector('#mansi-glow-value');
    let saved=100;
    try{saved=Number(localStorage.getItem('mansiAvatarGlowSensitivity'))||100;}catch(e){}
    slider.value=String(Math.max(35,Math.min(200,saved)));
    function apply(){
      const amount=Number(slider.value);
      window.MANSIAvatarGlowSensitivity=amount/100;
      output.textContent=amount+'%';
      try{localStorage.setItem('mansiAvatarGlowSensitivity',String(amount));}catch(e){}
    }
    slider.addEventListener('input',apply);
    apply();
    return true;
  }
  if(!mountSensitivity()){
    const observer=new MutationObserver(()=>{if(mountSensitivity())observer.disconnect();});
    observer.observe(document.documentElement,{childList:true,subtree:true});
    setTimeout(()=>observer.disconnect(),10000);
  }
})();
</script>
"""
    close = html.lower().rfind("</body>")
    if close >= 0: html = html[:close] + sensitivity_ui + "\\n" + html[close:]
    else: html += "\\n" + sensitivity_ui
    orb.write_text(html, encoding="utf-8")
    print("Added a persistent voice-glow intensity slider to the avatar customizer.")
else:
    print("Voice-glow intensity control already installed.")
