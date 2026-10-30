#!/usr/bin/env python3
"""Install MANSI's cute anime portrait with gentle idle, blink and orb reactions."""
from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main/assets")
orb = ROOT / "orb.html"
if not orb.is_file():
    raise SystemExit(f"Required orb asset not found: {orb}")
html = orb.read_text(encoding="utf-8")

# This build starts from the source ZIP, so replace the previous generated SVG safely.
avatar = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs>
 <linearGradient id="hair" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#282044"/><stop offset=".55" stop-color="#514078"/><stop offset="1" stop-color="#a36cc4"/></linearGradient>
 <linearGradient id="skin" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#fff0e9"/><stop offset="1" stop-color="#f4c5ce"/></linearGradient>
 <linearGradient id="coat" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b6a0ff"/><stop offset="1" stop-color="#ee9bdc"/></linearGradient>
 <radialGradient id="eye"><stop stop-color="#fff"/><stop offset=".32" stop-color="#ff8ed8"/><stop offset="1" stop-color="#7655b9"/></radialGradient>
</defs>
<!-- hair behind the face -->
<path d="M102 262C73 112 143 36 257 38c124 2 189 87 157 236l-8 151H111Z" fill="url(#hair)"/>
<path d="M128 186C143 89 213 56 276 67c-54 19-83 63-87 115-4 58-2 107-31 171-18-41-35-103-30-167Z" fill="#34264f"/>
<path d="M326 76c64 28 92 93 67 191-11 44-5 76 17 111-47-18-72-64-69-119 4-73 17-128-15-183Z" fill="#3b2a59"/>
<path d="M314 69c-13 42-43 69-86 87 36-6 73-24 99-53" fill="none" stroke="#c08bdf" stroke-width="13" stroke-linecap="round" opacity=".8"/>
<!-- neck and shoulders -->
<path d="M218 333h77v70c0 27-77 27-77 0Z" fill="url(#skin)"/>
<path d="M106 512c8-89 58-133 150-133s143 44 151 133Z" fill="url(#coat)"/>
<path d="M213 389l43 49 43-49-20-16h-46Z" fill="#fff1fb"/>
<path d="M246 439l10 14 10-14-10-18Z" fill="#f65dc8"/>
<!-- face -->
<path d="M157 179c0-75 43-116 101-116s101 41 101 116v104c0 75-47 122-101 122s-101-47-101-122Z" fill="url(#skin)"/>
<!-- fringe -->
<path d="M150 205c-8-81 32-143 109-143 70 0 111 48 106 128-23-5-43-28-55-60-21 31-65 51-116 51-14 0-29 11-44 24Z" fill="url(#hair)"/>
<path d="M155 179c-5 43 0 81 18 107-4-55 7-83 27-108-13 2-30 2-45 1Z" fill="#45315f"/>
<path d="M350 166c10 36 7 78-9 116 0-45-12-77-30-99 14-2 27-8 39-17Z" fill="#493363"/>
<!-- eyebrows -->
<path d="M188 224q28-19 53 0M271 224q28-19 53 0" fill="none" stroke="#76506e" stroke-width="7" stroke-linecap="round"/>
<!-- eyes with gentle periodic blinks -->
<ellipse cx="216" cy="258" rx="27" ry="34" fill="#fff"><animate attributeName="ry" values="34;2;34;34" keyTimes="0;.035;.075;1" dur="4.8s" begin="1.2s" repeatCount="indefinite"/></ellipse>
<ellipse cx="297" cy="258" rx="27" ry="34" fill="#fff"><animate attributeName="ry" values="34;2;34;34" keyTimes="0;.035;.075;1" dur="4.8s" begin="1.2s" repeatCount="indefinite"/></ellipse>
<ellipse cx="218" cy="263" rx="19" ry="27" fill="url(#eye)"><animate attributeName="ry" values="27;1;27;27" keyTimes="0;.035;.075;1" dur="4.8s" begin="1.2s" repeatCount="indefinite"/></ellipse>
<ellipse cx="295" cy="263" rx="19" ry="27" fill="url(#eye)"><animate attributeName="ry" values="27;1;27;27" keyTimes="0;.035;.075;1" dur="4.8s" begin="1.2s" repeatCount="indefinite"/></ellipse>
<ellipse cx="222" cy="253" rx="7" ry="10" fill="#fff"/>
<ellipse cx="299" cy="253" rx="7" ry="10" fill="#fff"/>
<path d="M188 243q28-30 55-1M270 242q28-29 55 1" fill="none" stroke="#453052" stroke-width="8" stroke-linecap="round"/>
<path d="M187 281q28 18 55 0M269 280q28 18 55 0" fill="none" stroke="#bd6f9b" stroke-width="4" stroke-linecap="round"/>
<!-- blush, nose, warm smile -->
<ellipse cx="183" cy="298" rx="20" ry="10" fill="#f29bb8" opacity=".45"/>
<ellipse cx="329" cy="298" rx="20" ry="10" fill="#f29bb8" opacity=".45"/>
<path d="M254 282q-7 12 2 14" fill="none" stroke="#d69a9e" stroke-width="3" stroke-linecap="round"/>
<path d="M235 321q21 22 43 0" fill="none" stroke="#c65e8c" stroke-width="5" stroke-linecap="round"/>
<!-- hair ornaments -->
<path d="M350 133l22-26 21 27-21 22Z" fill="#ff9bdf" stroke="#ffe2fa" stroke-width="5"/>
<circle cx="372" cy="130" r="7" fill="#fff"/>
<path d="M151 150l-17-21 22-19 19 21Z" fill="#9b8cff" stroke="#e9ddff" stroke-width="4"/>
</svg>'''
asset = ROOT / "mansi-anime-avatar.svg"
asset.write_text(avatar, encoding="utf-8")

# Remove an earlier generated injection if this script is re-run against an already patched tree.
html = re.sub(r'<img class="mansi-anime-avatar"[^>]*>', '', html)
html = re.sub(r'<style>\s*/\* MANSI_CUTE_ANIME_CENTER_AVATAR_V1 \*/.*?</style>', '', html, flags=re.S)

# Inject the portrait into the existing orb markup, leaving the pink heart element intact.
needle = "orb.innerHTML="
start = html.find(needle)
if start < 0:
    raise SystemExit("Could not find the MANSI orb innerHTML template; no unsafe rewrite performed.")
end = html.find(";", start)
if end < 0:
    raise SystemExit("Could not locate end of MANSI orb template.")
statement = html[start:end+1]
if "mansi-heart" not in statement:
    raise SystemExit("Expected heart markup was not found in the orb template.")
statement_new = statement.replace(
    '<div class="mansi-core"></div>',
    '<div class="mansi-core"></div><img class="mansi-anime-avatar" src="file:///android_asset/mansi-anime-avatar.svg" alt="MANSI anime girl"/>'
)
if statement_new == statement:
    raise SystemExit("Could not safely insert avatar into orb template.")
html = html[:start] + statement_new + html[end+1:]

css = r'''
<style>
/* MANSI_CUTE_ANIME_CENTER_AVATAR_V2 */
#mansi-final-orb .mansi-anime-avatar{
 position:absolute;z-index:3;left:50%;top:48%;transform:translate(-50%,-50%);
 width:48%;height:48%;object-fit:contain;object-position:center;
 filter:drop-shadow(0 2px 8px rgba(108,62,150,.22));
 pointer-events:none;user-select:none;-webkit-user-drag:none;
 animation:mansi-anime-idle 3.6s ease-in-out infinite;
}
#mansi-final-orb .mansi-heart{
 z-index:5!important;width:12%!important;height:12%!important;
 left:50%!important;top:76%!important;
 filter:drop-shadow(0 0 5px #ff65d9) drop-shadow(0 0 13px rgba(255,72,216,.85))!important;
}
#mansi-final-orb .mansi-core{overflow:hidden!important}
#mansi-final-orb.listening .mansi-anime-avatar{
 filter:drop-shadow(0 0 10px #67e6ff) brightness(1.07);
 animation:mansi-anime-listen 1.8s ease-in-out infinite;
}
#mansi-final-orb.speaking .mansi-anime-avatar{
 filter:drop-shadow(0 0 12px #ff75db) brightness(1.06);
 animation:mansi-anime-speak .48s ease-in-out infinite alternate;
}
@keyframes mansi-anime-idle{
 0%,100%{transform:translate(-50%,-50%) rotate(-.6deg)}
 50%{transform:translate(-50%,-51.2%) rotate(.6deg)}
}
@keyframes mansi-anime-listen{
 0%,100%{transform:translate(-50%,-50%) rotate(-1deg) scale(1)}
 50%{transform:translate(-50%,-51%) rotate(1deg) scale(1.018)}
}
@keyframes mansi-anime-speak{
 from{transform:translate(-50%,-50%) scale(1)}
 to{transform:translate(-50%,-51%) scale(1.025)}
}
@media(prefers-reduced-motion:reduce){
 #mansi-final-orb .mansi-anime-avatar{animation:none!important}
}
</style>
'''
if re.search(r"</body\s*>", html, re.I):
    html = re.sub(r"</body\s*>", css + "\n</body>", html, count=1, flags=re.I)
else:
    html += "\n" + css
orb.write_text(html, encoding="utf-8")
print("Installed animated MANSI anime portrait: blinking eyes, idle float, listening reaction and speaking motion; preserved pink heart.")


# Add expressive reactions without replacing the existing hologram or heart.
html = orb.read_text(encoding="utf-8")
extra = r"""
<style>
/* MANSI_ANIME_REACTIONS_V1 */
#mansi-final-orb .mansi-anime-avatar.mansi-wink { animation:mansi-wink .42s ease-in-out 1!important; }
#mansi-final-orb .mansi-anime-avatar.mansi-happy { filter:drop-shadow(0 0 13px #ff9be5) saturate(1.12); }
#mansi-final-orb .mansi-anime-avatar.mansi-shy { filter:drop-shadow(0 0 12px #ff8fca) hue-rotate(-8deg); }
#mansi-final-orb .mansi-anime-avatar.mansi-surprised { filter:drop-shadow(0 0 14px #9deaff) brightness(1.12); }
#mansi-final-orb .mansi-anime-avatar.mansi-sleepy { filter:brightness(.88) saturate(.82); opacity:.88; }
#mansi-final-orb.mansi-sleep-mode .mansi-anime-avatar { animation:none!important; filter:brightness(.72) saturate(.72)!important; }
#mansi-final-orb .mansi-heart-particle {
 position:absolute;z-index:8;left:50%;top:54%;pointer-events:none;
 color:#ff76cf;font-size:18px;text-shadow:0 0 9px #ff7bd9;
 animation:mansi-heart-float 1.25s ease-out forwards;
}
@keyframes mansi-wink { 0%,100%{transform:translate(-50%,-50%) scale(1)} 45%{transform:translate(-50%,-50%) scaleY(.91) scaleX(1.03)} }
@keyframes mansi-heart-float { 0%{opacity:0;transform:translate(-50%,0) scale(.55)} 20%{opacity:1} 100%{opacity:0;transform:translate(var(--dx),-85px) scale(1.25)} }
</style>
<script>
(function(){
 const orb=document.getElementById('mansi-final-orb');
 if(!orb || orb.dataset.mansiReactions==='1') return;
 orb.dataset.mansiReactions='1';
 const avatar=orb.querySelector('.mansi-anime-avatar');
 if(!avatar) return;
 const moods=['mansi-happy','mansi-shy','mansi-surprised'];
 let moodTimer=null, idleTimer=null;
 function clearMood(){avatar.classList.remove(...moods,'mansi-sleepy','mansi-wink');}
 function react(mood){clearMood(); if(mood) avatar.classList.add(mood);}
 function hearts(){
   for(let i=0;i<3;i++){
     const h=document.createElement('span'); h.className='mansi-heart-particle'; h.textContent='♥';
     h.style.setProperty('--dx', (Math.random()*90-45)+'px');
     h.style.left=(43+Math.random()*14)+'%'; h.style.top=(48+Math.random()*12)+'%';
     orb.appendChild(h); setTimeout(()=>h.remove(),1400);
   }
 }
 function resetIdle(){
   clearTimeout(idleTimer); orb.classList.remove('mansi-sleep-mode');
   react('mansi-happy');
   idleTimer=setTimeout(()=>{ if(!orb.classList.contains('listening')&&!orb.classList.contains('speaking')) react('mansi-sleepy'); },45000);
 }
 orb.addEventListener('click',function(){react('mansi-shy');hearts();resetIdle();});
 const observer=new MutationObserver(()=>{
   if(orb.classList.contains('listening')){react(null);clearTimeout(idleTimer);}
   else if(orb.classList.contains('speaking')){react('mansi-happy');clearTimeout(idleTimer);}
   else resetIdle();
 });
 observer.observe(orb,{attributes:true,attributeFilter:['class']});
 document.addEventListener('visibilitychange',()=>{
   if(document.hidden){orb.classList.add('mansi-sleep-mode');}
   else {orb.classList.remove('mansi-sleep-mode');resetIdle();}
 });
 function wink(){if(document.hidden||orb.classList.contains('mansi-sleep-mode'))return;
   avatar.classList.remove('mansi-wink');void avatar.offsetWidth;avatar.classList.add('mansi-wink');
 }
 setInterval(wink,8500);
 resetIdle();
})();
</script>
"""
if "MANSI_ANIME_REACTIONS_V1" not in html:
    html = re.sub(r"</body\\s*>", extra + "\\n</body>", html, count=1, flags=re.I) if re.search(r"</body\\s*>", html, re.I) else html + extra
    orb.write_text(html, encoding="utf-8")
print("Added anime reactions: wink, mood states, floating hearts, tap response and sleepy/visibility mode.")
