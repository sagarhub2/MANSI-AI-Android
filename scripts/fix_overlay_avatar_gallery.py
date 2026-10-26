from pathlib import Path

target = Path("source/mansi/app/src/main/assets/overlay-toys/gallery.html")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{--fg:#f5f3ff;--accent:#b78cff;--panel:rgba(22,20,48,.82)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;background:transparent;color:var(--fg);font-family:system-ui,-apple-system,sans-serif}
body{padding:10px 8px 18px}
.heading{text-align:center;font-size:15px;font-weight:800;letter-spacing:1.4px;margin:2px 0 4px}
.sub{text-align:center;font-size:11px;opacity:.72;margin:0 0 12px}
#gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;width:100%;max-width:520px;margin:0 auto}
.card{min-width:0;border:1px solid rgba(190,160,255,.25);border-radius:16px;background:var(--panel);padding:10px 3px 8px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--fg);font:inherit;cursor:pointer;min-height:98px;box-shadow:0 5px 18px rgba(0,0,0,.16);-webkit-tap-highlight-color:transparent}
.card:active{transform:scale(.97)}
.card.selected{border:2px solid var(--accent);background:rgba(112,65,190,.34);box-shadow:0 0 16px rgba(183,140,255,.38)}
.avatar{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;font-size:27px;background:radial-gradient(circle at 35% 25%,#5b70ff,#38205e 70%);border:1px solid rgba(255,255,255,.38);box-shadow:0 0 13px rgba(123,91,255,.3)}
.label{font-size:11px;font-weight:700;text-align:center;line-height:1.2}
.tick{font-size:9px;opacity:.8;min-height:10px}
@media(min-width:420px){#gallery{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-height:105px}}
</style>
</head>
<body>
<div class="heading">CHOOSE YOUR AVATAR</div>
<div class="sub">Tap a character to select it</div>
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
