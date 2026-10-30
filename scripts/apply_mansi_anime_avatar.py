#!/usr/bin/env python3
"""Install the cute anime-girl portrait into MANSI's existing pink-heart center orb."""
from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main/assets")
orb = ROOT / "orb.html"
if not orb.is_file():
    raise SystemExit(f"Required orb asset not found: {orb}")
html = orb.read_text(encoding="utf-8")
marker = "MANSI_CUTE_ANIME_CENTER_AVATAR_V1"
if marker in html:
    print("MANSI anime center avatar already installed.")
    raise SystemExit(0)

# Original, locally bundled SVG: no remote image request and no runtime network dependency.
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
<!-- eyes -->
<ellipse cx="216" cy="258" rx="27" ry="34" fill="#fff"/>
<ellipse cx="297" cy="258" rx="27" ry="34" fill="#fff"/>
<ellipse cx="218" cy="263" rx="19" ry="27" fill="url(#eye)"/>
<ellipse cx="295" cy="263" rx="19" ry="27" fill="url(#eye)"/>
<ellipse cx="222" cy="253" rx="7" ry="10" fill="#fff"/>
<ellipse cx="299" cy="253" rx="7" ry="10" fill="#fff"/>
<path d="M188 243q28-30 55-1M270 242q28-29 55 1" fill="none" stroke="#453052" stroke-width="8" stroke-linecap="round"/>
<path d="M187 281q28 18 55 0M269 280q28 18 55 0" fill="none" stroke="#bd6f9b" stroke-width="4" stroke-linecap="round"/>
<!-- blush, nose, smile -->
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
/* MANSI_CUTE_ANIME_CENTER_AVATAR_V1 */
#mansi-final-orb .mansi-anime-avatar{
 position:absolute;z-index:3;left:50%;top:48%;transform:translate(-50%,-50%);
 width:48%;height:48%;object-fit:contain;object-position:center;
 filter:drop-shadow(0 2px 8px rgba(108,62,150,.22));
 pointer-events:none;user-select:none;-webkit-user-drag:none;
}
#mansi-final-orb .mansi-heart{
 z-index:5!important;width:12%!important;height:12%!important;
 left:50%!important;top:76%!important;
 filter:drop-shadow(0 0 5px #ff65d9) drop-shadow(0 0 13px rgba(255,72,216,.85))!important;
}
#mansi-final-orb .mansi-core{overflow:hidden!important}
#mansi-final-orb.listening .mansi-anime-avatar{filter:drop-shadow(0 0 10px #67e6ff) brightness(1.04)}
#mansi-final-orb.speaking .mansi-anime-avatar{animation:mansi-anime-speak 0.42s ease-in-out infinite alternate}
@keyframes mansi-anime-speak{from{transform:translate(-50%,-50%) scale(1)}to{transform:translate(-50%,-51%) scale(1.025)}}
@media(prefers-reduced-motion:reduce){#mansi-final-orb .mansi-anime-avatar{animation:none!important}}
</style>
'''
if re.search(r"</body\s*>", html, re.I):
    html = re.sub(r"</body\s*>", css + "\n</body>", html, count=1, flags=re.I)
else:
    html += "\n" + css
orb.write_text(html, encoding="utf-8")
print("Installed local anime-girl SVG in MANSI center orb; preserved existing pink heart and orb state classes.")
