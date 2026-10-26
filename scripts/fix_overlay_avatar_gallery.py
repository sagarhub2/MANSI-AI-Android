from pathlib import Path

target = Path("source/mansi/app/src/main/assets/overlay-toys/gallery.html")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{--fg:#f6f3ff;--accent:#ffdf70;--panel:rgba(16,10,34,.82)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;background:transparent;color:var(--fg);font-family:system-ui,-apple-system,sans-serif}
body{position:relative;isolation:isolate;overflow:hidden;padding:13px 8px 20px;background:radial-gradient(ellipse at 50% 0%,rgba(122,44,168,.28),transparent 62%),radial-gradient(ellipse at 0% 70%,rgba(31,100,153,.16),transparent 45%)}
body:before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.32;background-image:radial-gradient(1px 1px at 14% 20%,#fff 98%,transparent),radial-gradient(1px 1px at 78% 17%,#ffd7ff 98%,transparent),radial-gradient(1px 1px at 43% 68%,#a8f7ff 98%,transparent),radial-gradient(1px 1px at 88% 83%,#fff 98%,transparent);background-size:83px 91px;animation:starDrift 18s linear infinite}
.heading{text-align:center;font-size:17px;font-weight:950;letter-spacing:2.4px;margin:3px 0 5px;background:linear-gradient(90deg,#a8f7ff,#f0a6ff,#ffdf70);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 10px rgba(205,125,255,.35))}
.sub{text-align:center;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:#c7b8ed;margin:0 0 14px}
#gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;width:100%;max-width:540px;margin:0 auto}
.card{position:relative;overflow:hidden;min-width:0;border:1px solid rgba(214,160,255,.3);border-radius:24px 10px 24px 10px;background:linear-gradient(145deg,rgba(50,25,73,.78),rgba(10,15,38,.91));padding:12px 3px 9px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;color:var(--fg);font:inherit;cursor:pointer;min-height:108px;box-shadow:inset 0 1px rgba(255,255,255,.09),0 8px 20px rgba(0,0,0,.22);-webkit-tap-highlight-color:transparent;transition:transform .22s,border-color .22s,box-shadow .22s}
.card:before{content:"";position:absolute;inset:-60% -30%;pointer-events:none;background:conic-gradient(from 0deg,transparent 0 72%,rgba(255,223,112,.18) 80%,transparent 88%);animation:orbit 8s linear infinite}
.card:after{content:"";position:absolute;left:12%;right:12%;top:8px;height:1px;background:linear-gradient(90deg,transparent,#f0a6ff,transparent);opacity:.65}
.card:active{transform:scale(.95) rotate(-1deg)}
.card.selected{border:1.5px solid var(--accent);border-radius:10px 24px 10px 24px;background:linear-gradient(145deg,rgba(92,42,105,.88),rgba(16,34,61,.95));box-shadow:0 0 0 1px rgba(255,223,112,.14),0 0 24px rgba(240,166,255,.24),inset 0 0 18px rgba(255,223,112,.07)}
.avatar{position:relative;width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-size:29px;background:radial-gradient(circle at 32% 22%,#f5c9ff,#8d46b5 47%,#1d1743 82%);border:1px solid rgba(255,218,255,.7);box-shadow:0 0 0 4px rgba(240,166,255,.07),0 0 19px rgba(216,103,255,.32),inset 0 0 13px rgba(255,255,255,.18);animation:floaty 3.4s ease-in-out infinite}
.card:nth-child(3n+2) .avatar{background:radial-gradient(circle at 32% 22%,#fff0ad,#c57a35 48%,#392044 82%);border-color:rgba(255,229,156,.75);box-shadow:0 0 0 4px rgba(255,223,112,.07),0 0 18px rgba(255,190,72,.24)}
.card:nth-child(3n) .avatar{background:radial-gradient(circle at 32% 22%,#b5ffed,#258eae 48%,#102440 82%);border-color:rgba(149,255,239,.72);box-shadow:0 0 0 4px rgba(83,243,255,.06),0 0 18px rgba(32,225,255,.23)}
.label{font-size:11px;font-weight:850;letter-spacing:.45px;text-align:center;line-height:1.2}
.tick{font-size:9px;letter-spacing:.7px;color:var(--accent);font-weight:900;min-height:10px}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-4px) rotate(2deg)}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes starDrift{to{background-position:83px 91px}}
@media(min-width:420px){#gallery{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-height:116px}}
</style>
</head>
<body>
<div class="heading">MANSI ✦ COSMIC REALM</div>
<div class="sub">✧ Pick a companion from another dimension ✧</div>
<div id="gallery" role="list">
<button class="card" data-name="droid" onclick="choose(this)"><span class="avatar">🤖</span><span class="label">Droid</span><span class="tick"></span></button>
<button class="card" data-name="mech" onclick="choose(this)"><span class="avatar">🦾</span><span class="label">Mech</span><span class="tick"></span></button>
<button class="card" data-name="blob" onclick="choose(this)"><span class="avatar">🫧</span><span class="label">Blob</span><span class="tick"></span></button>
<button class="card" data-name="cloud" onclick="choose(this)"><span class="avatar">☁️</span><span class="label">Cloud</span><span class="tick"></span></button>
<button class="card" data-name="puddle" onclick="choose(this)"><span class="avatar">💧</span><span class="label">Puddle</span><span class="tick"></span></button>
<button class="card" data-name="star" onclick="choose(this)"><span class="avatar">⭐</span><span class="label">Star</span><span class="tick"></span></button>
<button class="card" data-name="alien" onclick="choose(this)"><span class="avatar">👽</span><span class="label">Alien</span><span class="tick"></span></button>
<button class="card" data-name="circle" onclick="choose(this)"><span class="avatar">🔵</span><span class="label">Circle</span><span class="tick"></span></button>
<button class="card" data-name="triangle" onclick="choose(this)"><span class="avatar">🔺</span><span class="label">Triangle</span><span class="tick"></span></button>
<button class="card" data-name="flower" onclick="choose(this)"><span class="avatar">🌸</span><span class="label">Flower</span><span class="tick"></span></button>
<button class="card" data-name="pill" onclick="choose(this)"><span class="avatar">💊</span><span class="label">Pill</span><span class="tick"></span></button>
<button class="card" data-name="square" onclick="choose(this)"><span class="avatar">🟪</span><span class="label">Square</span><span class="tick"></span></button>
<button class="card" data-name="hexagon" onclick="choose(this)"><span class="avatar">⬡</span><span class="label">Hexagon</span><span class="tick"></span></button>
<button class="card" data-name="cat" onclick="choose(this)"><span class="avatar">🐱</span><span class="label">Cat</span><span class="tick"></span></button>
<button class="card" data-name="pebble" onclick="choose(this)"><span class="avatar">🪨</span><span class="label">Pebble</span><span class="tick"></span></button>
<button class="card" data-name="ghost" onclick="choose(this)"><span class="avatar">👻</span><span class="label">Ghost</span><span class="tick"></span></button>
<button class="card" data-name="drop" onclick="choose(this)"><span class="avatar">🔮</span><span class="label">Crystal</span><span class="tick"></span></button>
</div>
<script>
function choose(card){
 document.querySelectorAll('.card').forEach(x=>{x.classList.remove('selected');x.querySelector('.tick').textContent='';});
 card.classList.add('selected');card.querySelector('.tick').textContent='✓ SELECTED';
 try{if(window.JarvisAvatarPicker&&window.JarvisAvatarPicker.selectAvatar)window.JarvisAvatarPicker.selectAvatar(card.dataset.name);}catch(e){}
}
window.setSelectedAvatar=function(name){document.querySelectorAll('.card').forEach(x=>{const yes=x.dataset.name===name;x.classList.toggle('selected',yes);x.querySelector('.tick').textContent=yes?'✓ SELECTED':'';});};
window.setGalleryTheme=function(fg,accent){if(fg)document.documentElement.style.setProperty('--fg',fg);if(accent)document.documentElement.style.setProperty('--accent',accent);};
window.addEventListener('load',()=>{try{if(window.JarvisAvatarPicker&&window.JarvisAvatarPicker.pageReady)window.JarvisAvatarPicker.pageReady();}catch(e){}});
</script>
</body></html>
""", encoding="utf-8")
print("FIXED overlay avatar gallery: wrote visible responsive selectable avatar grid to", target)
