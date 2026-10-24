#!/usr/bin/env python3
"""Apply the MANSI AI gender-neutral hologram orb to the packaged WebView asset."""
from pathlib import Path
import re

asset = Path("source/mansi/app/src/main/assets/orb.html")
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "/* MANSI_FINAL_HOLOGRAM_ORB_V1 */"
if marker in html:
    print("MANSI hologram orb patch already present.")
    raise SystemExit(0)

patch = r"""
<style>
/* MANSI_FINAL_HOLOGRAM_ORB_V1 */
#mansi-final-orb{position:relative!important;display:grid!important;place-items:center!important;width:min(76vw,330px)!important;aspect-ratio:1/1!important;margin:0 auto!important;border-radius:50%!important;isolation:isolate;cursor:pointer;touch-action:manipulation;outline:none;user-select:none;-webkit-tap-highlight-color:transparent}
#mansi-final-orb .mansi-core{position:absolute;inset:25%;border-radius:50%;background:radial-gradient(circle at 35% 28%,rgba(255,255,255,.35),transparent 20%),radial-gradient(circle at 50% 60%,#15114c 0%,#08091d 64%,#03040d 100%);border:1px solid rgba(161,126,255,.7);box-shadow:inset 0 0 28px rgba(68,102,255,.55),0 0 26px rgba(106,83,255,.6),0 0 65px rgba(222,71,255,.22);transition:box-shadow .25s ease,transform .25s ease}
#mansi-final-orb .mansi-ring{position:absolute;inset:var(--inset);border-radius:50%;border:2px solid transparent;background:linear-gradient(#050616,#050616) padding-box,conic-gradient(from var(--angle,0deg),#3de8ff,#5268ff,#c34cff,#ff83e9,#3de8ff) border-box;box-shadow:0 0 12px rgba(91,111,255,.5),inset 0 0 12px rgba(190,77,255,.13);animation:mansi-orbit var(--speed) linear infinite}
#mansi-final-orb .mansi-ring:after{content:"";position:absolute;inset:-5px;border-radius:50%;border:1px solid rgba(75,208,255,.18)}
#mansi-final-orb .mansi-ring.r1{--inset:5%;--speed:12s}
#mansi-final-orb .mansi-ring.r2{--inset:14%;--speed:8s;animation-direction:reverse;border-width:1px}
#mansi-final-orb .mansi-ring.r3{--inset:22%;--speed:16s;border-width:3px}
#mansi-final-orb .mansi-spark{position:absolute;width:6px;height:6px;border-radius:50%;background:#ff9bf2;box-shadow:0 0 12px #ec70ff,0 0 22px #697dff;top:50%;left:50%;transform:rotate(var(--a)) translateX(var(--r));}
#mansi-final-orb .mansi-tapwave{position:absolute;inset:18%;border:2px solid #a45bff;border-radius:50%;opacity:0;pointer-events:none}
#mansi-final-orb.active{filter:brightness(1.25)}
#mansi-final-orb.active .mansi-core{transform:scale(1.045);box-shadow:inset 0 0 38px rgba(68,102,255,.85),0 0 40px #5268ff,0 0 95px rgba(222,71,255,.8)}
#mansi-final-orb.active .mansi-tapwave{animation:mansi-tapwave .85s ease-out 2}
#mansi-final-orb.listening .mansi-ring{animation-duration:3s;box-shadow:0 0 18px #3de8ff,inset 0 0 15px rgba(61,232,255,.3)}
#mansi-final-orb.speaking .mansi-ring{animation:mansi-speaking 1.1s ease-in-out infinite alternate}
#mansi-final-orb.idle .mansi-core{animation:mansi-breathe 3s ease-in-out infinite}
@keyframes mansi-orbit{to{transform:rotate(360deg)}}
@keyframes mansi-tapwave{0%{transform:scale(.7);opacity:.95}100%{transform:scale(1.65);opacity:0}}
@keyframes mansi-speaking{from{transform:scale(.97);filter:brightness(1)}to{transform:scale(1.035);filter:brightness(1.5)}}
@keyframes mansi-breathe{0%,100%{box-shadow:inset 0 0 20px rgba(68,102,255,.4),0 0 22px rgba(106,83,255,.4)}50%{box-shadow:inset 0 0 32px rgba(68,102,255,.7),0 0 42px rgba(222,71,255,.5)}}
@media(prefers-reduced-motion:reduce){#mansi-final-orb *,#mansi-final-orb{animation-duration:0.01ms!important;animation-iteration-count:1!important}}
</style>
<script>
(function(){
 function install(){
   if(document.getElementById('mansi-final-orb')) return;
   /* Hide legacy heart/logo glyphs without hiding the page's controls. */
   document.querySelectorAll('[id*="heart" i],[class*="heart" i],[aria-label*="heart" i]').forEach(function(el){
     if(el.matches('svg,img,i,span,div') && !el.closest('button,input,a')) el.style.display='none';
   });
   var orb=document.createElement('div');
   orb.id='mansi-final-orb';orb.className='idle';orb.setAttribute('role','button');orb.setAttribute('tabindex','0');orb.setAttribute('aria-label','Activate MANSI AI');
   orb.innerHTML='<div class="mansi-ring r1"></div><div class="mansi-ring r2"></div><div class="mansi-ring r3"></div><div class="mansi-core"></div><div class="mansi-tapwave"></div><i class="mansi-spark" style="--a:0deg;--r:47%"></i><i class="mansi-spark" style="--a:120deg;--r:47%"></i><i class="mansi-spark" style="--a:240deg;--r:47%"></i>';
   var host=document.querySelector('#orb, .orb, [class*="orb" i], main, body');
   if(!host) host=document.body;
   if(host===document.body){orb.style.position='fixed';orb.style.left='50%';orb.style.top='50%';orb.style.transform='translate(-50%,-50%)';orb.style.zIndex='99999';}
   host.appendChild(orb);
   function activate(){orb.classList.remove('idle');orb.classList.add('active');setTimeout(function(){orb.classList.remove('active');orb.classList.add('idle')},1800);}
   orb.addEventListener('click',activate);orb.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();activate()}});
   window.MANSIOrbState=function(state){orb.classList.remove('idle','listening','speaking');orb.classList.add(['idle','listening','speaking'].indexOf(state)>=0?state:'idle')};
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
"""
# Append at the end so the final orb CSS wins over earlier visual rules.
if re.search(r"</body\s*>", html, re.I):
    html = re.sub(r"</body\s*>", patch + "\n</body>", html, count=1, flags=re.I)
else:
    html += "\n" + patch
asset.write_text(html, encoding="utf-8")
print("Applied MANSI hologram rings + tap glow to", asset)
