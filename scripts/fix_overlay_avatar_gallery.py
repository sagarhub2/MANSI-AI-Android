from pathlib import Path

target = Path("source/mansi/app/src/main/assets/overlay-toys/gallery.html")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{--fg:#f4fbff;--accent:#53f3ff;--panel:rgba(7,17,39,.76)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;background:transparent;color:var(--fg);font-family:system-ui,-apple-system,sans-serif}
body{padding:12px 8px 20px;background:radial-gradient(ellipse at 50% 0%,rgba(36,83,190,.22),transparent 68%)}
.heading{text-align:center;font-size:16px;font-weight:900;letter-spacing:2.6px;margin:3px 0 5px;text-shadow:0 0 16px rgba(83,243,255,.52)}
.sub{text-align:center;font-size:10px;letter-spacing:1.3px;text-transform:uppercase;color:#9ec8ff;margin:0 0 14px}
#gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;width:100%;max-width:540px;margin:0 auto}
.card{position:relative;overflow:hidden;min-width:0;border:1px solid rgba(91,194,255,.24);border-radius:19px;background:linear-gradient(145deg,rgba(23,43,83,.86),rgba(7,12,30,.88));padding:12px 3px 9px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;color:var(--fg);font:inherit;cursor:pointer;min-height:105px;box-shadow:inset 0 1px rgba(255,255,255,.07),0 7px 18px rgba(0,0,0,.2);-webkit-tap-highlight-color:transparent;transition:transform .18s,border-color .18s,box-shadow .18s}
.card:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 20%,rgba(83,243,255,.08),transparent 65%);transform:translateX(-100%);transition:transform .4s}
.card:active{transform:scale(.96)}
.card.selected{border:1.5px solid var(--accent);background:linear-gradient(145deg,rgba(15,87,124,.85),rgba(30,24,83,.94));box-shadow:0 0 0 1px rgba(83,243,255,.16),0 0 23px rgba(83,243,255,.22),inset 0 0 18px rgba(83,243,255,.08)}
.card.selected:before{transform:translateX(100%)}
.avatar{position:relative;width:54px;height:54px;border-radius:18px;display:grid;place-items:center;font-size:29px;background:radial-gradient(circle at 32% 22%,#4eeaff,#3b4fe0 47%,#19163e 80%);border:1px solid rgba(147,240,255,.58);box-shadow:0 0 18px rgba(48,194,255,.28),inset 0 0 13px rgba(255,255,255,.15);animation:floaty 3s ease-in-out infinite}
.card:nth-child(3n+2) .avatar{background:radial-gradient(circle at 32% 22%,#ffb8f5,#a43fd2 48%,#251044 82%);border-color:rgba(255,174,245,.6);box-shadow:0 0 18px rgba(232,80,255,.24)}
.card:nth-child(3n) .avatar{background:radial-gradient(circle at 32% 22%,#b5ffdf,#14a994 48%,#102d48 82%);border-color:rgba(149,255,219,.6);box-shadow:0 0 18px rgba(32,255,194,.2)}
.label{font-size:11px;font-weight:800;letter-spacing:.35px;text-align:center;line-height:1.2}
.tick{font-size:9px;letter-spacing:.7px;color:var(--accent);font-weight:800;min-height:10px}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@media(min-width:420px){#gallery{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-height:112px}}
</style>
</head>
<body>
<div class="heading">MANSI · AVATAR LAB</div>
<div class="sub">✦ Choose your hologram companion ✦</div>
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
