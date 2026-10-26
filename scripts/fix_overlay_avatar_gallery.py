from pathlib import Path

target = Path("source/mansi/app/src/main/assets/overlay-toys/gallery.html")
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{--fg:#f4f1ff;--accent:#bba2ff}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;background:transparent;color:var(--fg);font-family:system-ui,-apple-system,sans-serif}
body{padding:12px 8px 18px;overflow:auto}
.heading{text-align:center;font-size:16px;font-weight:800;letter-spacing:1.5px;margin:3px 0 5px;color:#f4f1ff}
.sub{text-align:center;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#c9c0dd;margin:0 0 14px}
#gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;width:100%;max-width:540px;margin:0 auto}
.card{min-width:0;border:1px solid #625876;border-radius:12px;background:rgba(28,24,42,.78);padding:10px 3px 8px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;color:var(--fg);font:inherit;cursor:pointer;min-height:100px;-webkit-tap-highlight-color:transparent}
.card.selected{border:2px solid var(--accent);background:rgba(70,54,99,.9)}
.avatar{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-size:29px;background:rgba(70,62,91,.7);border:1px solid #807494}
.label{font-size:11px;font-weight:750;letter-spacing:.3px;text-align:center;line-height:1.2}
.tick{font-size:9px;letter-spacing:.5px;color:var(--accent);font-weight:800;min-height:10px}
@media(min-width:420px){#gallery{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-height:108px}}
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
