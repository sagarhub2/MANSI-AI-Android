#!/usr/bin/env python3
"""Apply the MANSI AI gender-neutral hologram orb to the packaged WebView asset."""
from pathlib import Path
import re

asset = Path("source/mansi/app/src/main/assets/orb.html")
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "/* MANSI_FINAL_HOLOGRAM_ORB_V3 */"
if marker in html:
    print("MANSI hologram orb patch already present.")
    raise SystemExit(0)

patch = r"""
<style>
/* MANSI_FINAL_HOLOGRAM_ORB_V3 */
#mansi-final-orb{position:fixed!important;left:50%!important;top:26.5%!important;transform:translate(-50%,-50%)!important;display:grid!important;place-items:center!important;width:min(56vw,380px)!important;height:min(56vw,380px)!important;aspect-ratio:1/1!important;margin:0!important;border-radius:50%!important;isolation:isolate;cursor:pointer;touch-action:manipulation;outline:none;user-select:none;-webkit-tap-highlight-color:transparent}
#mansi-final-orb .mansi-core{position:absolute;inset:25%;border-radius:50%;background:radial-gradient(circle at 35% 28%,rgba(255,255,255,.35),transparent 20%),radial-gradient(circle at 50% 60%,#15114c 0%,#08091d 64%,#03040d 100%);border:1px solid rgba(161,126,255,.7);box-shadow:inset 0 0 28px rgba(68,102,255,.55),0 0 26px rgba(106,83,255,.6),0 0 65px rgba(222,71,255,.22);transition:box-shadow .25s ease,transform .25s ease}
#mansi-final-orb .mansi-heart{position:absolute;z-index:4;width:19%;height:19%;left:50%;top:48%;transform:translate(-50%,-50%);filter:drop-shadow(0 0 7px #ff74e8) drop-shadow(0 0 18px #9d5cff);animation:mansi-heartbeat 2s ease-in-out infinite;pointer-events:none}
#mansi-final-orb .mansi-heart path{fill:url(#mansiHeartGradient);stroke:#ffc5fb;stroke-width:1.5}
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
@keyframes mansi-heartbeat{0%,100%{transform:translate(-50%,-50%) scale(1)}50%{transform:translate(-50%,-50%) scale(1.13)}}
@keyframes mansi-orbit{to{transform:rotate(360deg)}}
@keyframes mansi-tapwave{0%{transform:scale(.7);opacity:.95}100%{transform:scale(1.65);opacity:0}}
@keyframes mansi-speaking{from{transform:scale(.97);filter:brightness(1)}to{transform:scale(1.035);filter:brightness(1.5)}}
@keyframes mansi-breathe{0%,100%{box-shadow:inset 0 0 20px rgba(68,102,255,.4),0 0 22px rgba(106,83,255,.4)}50%{box-shadow:inset 0 0 32px rgba(68,102,255,.7),0 0 42px rgba(222,71,255,.5)}}
@media(prefers-reduced-motion:reduce){#mansi-final-orb *,#mansi-final-orb{animation-duration:0.01ms!important;animation-iteration-count:1!important}}
</style>
<style>
/* MANSI_CLEAN_BG_V5 — remove stray legacy orb lines and oversized halo */
html,body{overflow-x:hidden!important}
body::before,body::after,html::before,html::after{content:none!important;display:none!important;background:none!important;box-shadow:none!important;border:0!important}
#mansi-final-orb{width:min(56vw,300px)!important;height:min(56vw,300px)!important;top:27.5%!important;left:50%!important;overflow:visible!important;filter:none!important;box-shadow:none!important;border:0!important;background:transparent!important;outline:0!important}
#mansi-final-orb::before,#mansi-final-orb::after{content:none!important;display:none!important}
#mansi-final-orb .mansi-core{inset:0!important;border-radius:50%!important;background:radial-gradient(circle at 38% 30%,#fffaff 0%,#fff0fb 48%,#f8dcfa 78%,#f4d4fa 100%)!important;box-shadow:0 0 14px rgba(255,87,218,.7),0 0 34px rgba(255,62,211,.55),0 0 58px rgba(210,94,255,.26)!important;border:1px solid rgba(255,255,255,.65)!important}
#mansi-final-orb .mansi-heart{width:18%!important;height:18%!important;top:50%!important;left:50%!important;transform:translate(-50%,-50%)!important}
#mansi-final-orb .mansi-tapwave{display:none!important}
#mansi-final-orb.active .mansi-core{animation:mansi-soft-breathe .7s ease-in-out 2!important}
/* MANSI_SOFT_PINK_ORB_V4 — match reference screenshot 2 */
#mansi-final-orb{width:min(56vw,300px)!important;height:min(56vw,300px)!important;top:27.5%!important;filter:none!important}
#mansi-final-orb .mansi-ring{display:none!important}
#mansi-final-orb .mansi-core{inset:19%!important;background:radial-gradient(circle at 35% 28%,#fffaff 0%,#fff0fb 42%,#f8dcfa 75%,#f4d4fa 100%)!important;border:0!important;box-shadow:0 0 12px rgba(255,87,218,.75),0 0 32px rgba(255,62,211,.7),0 0 68px rgba(210,94,255,.45),0 0 115px rgba(148,107,255,.2)!important}
#mansi-final-orb .mansi-heart{width:18%!important;height:18%!important;top:50%!important;filter:drop-shadow(0 0 5px #ff65d9) drop-shadow(0 0 12px rgba(255,72,216,.8))!important}
#mansi-final-orb .mansi-heart path{fill:#f45acb!important;stroke:#ff8be4!important;stroke-width:1!important}
#mansi-final-orb .mansi-tapwave{inset:19%!important;border-color:#f34dcc!important;box-shadow:0 0 18px #fa66df!important}
#mansi-final-orb.active .mansi-core{transform:scale(1.055)!important;box-shadow:0 0 20px #ff5edc,0 0 55px rgba(255,65,214,.95),0 0 100px rgba(177,92,255,.65)!important}
#mansi-final-orb.idle .mansi-core{animation:mansi-soft-breathe 2.8s ease-in-out infinite!important}
@keyframes mansi-soft-breathe{0%,100%{transform:scale(1);box-shadow:0 0 12px rgba(255,87,218,.65),0 0 32px rgba(255,62,211,.55),0 0 68px rgba(210,94,255,.35)}50%{transform:scale(1.035);box-shadow:0 0 20px rgba(255,87,218,.9),0 0 48px rgba(255,62,211,.75),0 0 88px rgba(210,94,255,.5)}}
</style>
<style>
/* MANSI_HEART_BACKGROUND_CLEAN_V2 — remove stray circle outlines, streaks and background layers */
html,body{background:transparent!important;background-image:none!important;overflow:hidden!important}
body{isolation:isolate!important}
body::before,body::after,html::before,html::after{display:none!important;content:none!important;background:none!important;border:0!important;outline:0!important;box-shadow:none!important}
#mansi-final-orb{background:transparent!important;border:0!important;outline:0!important;box-shadow:none!important;filter:none!important}
#mansi-final-orb .mansi-core{border:0!important;outline:0!important;border-radius:50%!important;box-shadow:0 0 18px rgba(255,87,218,.48),0 0 38px rgba(255,62,211,.22)!important}
#mansi-final-orb .mansi-heart{border:0!important;outline:0!important;box-shadow:none!important}
#mansi-final-orb .mansi-ring,#mansi-final-orb .mansi-tapwave{display:none!important;visibility:hidden!important}
body canvas,body svg:not(#mansi-final-orb svg){display:none!important;visibility:hidden!important}
body *{outline:none!important;-webkit-tap-highlight-color:transparent}
/* MANSI_HEART_CIRCLE_SOFT_BG_V3 — restore a soft luminous pink-lilac circle, not black */
#mansi-final-orb{background:transparent!important}
#mansi-final-orb .mansi-core{background:radial-gradient(circle at 34% 27%,#ffffff 0%,#fff5ff 26%,#ffe6fb 54%,#f8c9f2 76%,#e8b8f5 100%)!important;border:1px solid rgba(255,255,255,.78)!important;box-shadow:0 0 14px rgba(255,126,226,.72),0 0 32px rgba(255,105,220,.55),0 0 62px rgba(190,118,255,.3),inset 0 0 18px rgba(255,255,255,.72)!important}
#mansi-final-orb .mansi-heart{filter:drop-shadow(0 0 5px #ff65d9) drop-shadow(0 0 13px rgba(255,72,216,.78))!important}
#mansi-final-orb .mansi-heart path{fill:#f45acb!important;stroke:#ff9be9!important;stroke-width:1!important}
#mansi-final-orb.active .mansi-core{background:radial-gradient(circle at 34% 27%,#ffffff 0%,#fff2fe 28%,#ffd8f8 58%,#f3b5ed 100%)!important;box-shadow:0 0 20px rgba(255,100,220,.92),0 0 48px rgba(255,65,214,.72),0 0 82px rgba(177,92,255,.42)!important}
/* MANSI_REMOVE_ORB_LINES_V1 — keep the heart orb clean, without visible rings/contour bands */
#mansi-final-orb .mansi-ring,
#mansi-final-orb .mansi-ring::before,
#mansi-final-orb .mansi-ring::after,
#mansi-final-orb .mansi-tapwave{display:none!important;content:none!important}
#mansi-final-orb,
#mansi-final-orb::before,
#mansi-final-orb::after{border:0!important;outline:0!important;background:transparent!important}
#mansi-final-orb .mansi-core{border:0!important;outline:0!important;background:radial-gradient(circle at 38% 30%,#fffaff 0%,#fff2fb 52%,#f8e0fa 100%)!important;box-shadow:0 0 22px rgba(255,87,218,.62),0 0 48px rgba(255,62,211,.34)!important}
#mansi-final-orb.active .mansi-core{box-shadow:0 0 28px rgba(255,87,218,.78),0 0 58px rgba(255,62,211,.5)!important}
</style>
<script>
(function(){
 function install(){
   var previous=document.getElementById('mansi-final-orb');if(previous)previous.remove();
   /* Preserve the heart identity inside the new hologram; hide only the old standalone orb container if safe. */
   var orb=document.createElement('div');
   orb.id='mansi-final-orb';orb.className='idle';orb.setAttribute('role','button');orb.setAttribute('tabindex','0');orb.setAttribute('aria-label','Activate MANSI AI');
   orb.innerHTML='<div class="mansi-ring r1"></div><div class="mansi-ring r2"></div><div class="mansi-ring r3"></div><div class="mansi-core"></div><svg class="mansi-heart" viewBox="0 0 100 90" aria-hidden="true"><defs><linearGradient id="mansiHeartGradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ffb3f4"/><stop offset="48%" stop-color="#f05cff"/><stop offset="100%" stop-color="#6b8cff"/></linearGradient></defs><path d="M50 82 12 45C-7 23 9 2 29 5c10 1 17 8 21 16C58 9 67 4 78 6c20 4 27 26 10 43Z"/></svg><div class="mansi-tapwave"></div>';
   /* Viewport-level positioning avoids clipping by legacy orb containers. */
   var host=document.body;
   orb.style.position='fixed';orb.style.left='50%';orb.style.top='26.5%';orb.style.transform='translate(-50%,-50%)';orb.style.zIndex='99999';
   host.appendChild(orb);
   /* Remove the legacy orb/heart layer that caused two glowing circles to overlap. */
   Array.prototype.forEach.call(document.querySelectorAll('[id*="orb" i],[class*="orb" i],[id*="heart" i],[class*="heart" i]'),function(el){
     if(el===orb || orb.contains(el) || el.contains(orb)) return;
     if(el.closest && el.closest('#mansi-final-orb')) return;
     el.style.setProperty('display','none','important');
     el.setAttribute('aria-hidden','true');
   });
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
