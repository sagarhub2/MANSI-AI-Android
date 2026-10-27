from pathlib import Path

path = Path("source/mansi/app/src/main/assets/orb.html")
if not path.exists():
    raise SystemExit("orb.html missing; cannot apply MANSI Theme Studio safely.")
html = path.read_text(encoding="utf-8")
marker = "MANSI_THEME_STUDIO_V1"
if marker in html:
    print("MANSI 12-theme studio already present.")
    raise SystemExit(0)

block = r"""
<!-- MANSI_THEME_STUDIO_V1: 12 gender-neutral themes with persistent selection -->
<style>
#mansi-theme-open{position:fixed;right:14px;top:64px;z-index:99998;border:1px solid var(--mansi-accent,#258bff);border-radius:999px;padding:9px 13px;background:rgba(8,14,32,.86);color:#fff;font:600 13px system-ui,sans-serif;box-shadow:0 0 16px color-mix(in srgb,var(--mansi-accent,#258bff) 48%,transparent);backdrop-filter:blur(12px)}
#mansi-theme-panel{position:fixed;right:12px;top:108px;z-index:99999;width:min(310px,calc(100vw - 28px));max-height:68vh;overflow:auto;display:none;padding:14px;border:1px solid var(--mansi-accent,#258bff);border-radius:20px;background:rgba(8,12,28,.96);color:#fff;font:14px system-ui,sans-serif;box-shadow:0 12px 40px #0008;backdrop-filter:blur(18px)}
#mansi-theme-panel.open{display:block}
#mansi-theme-panel h3{margin:0 0 5px;font-size:16px}
#mansi-theme-panel p{margin:0 0 12px;color:#b9c5df;font-size:12px}
#mansi-theme-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
#mansi-theme-grid button{display:flex;align-items:center;gap:8px;text-align:left;min-height:48px;padding:8px;border:1px solid #ffffff30;border-radius:12px;background:#ffffff0c;color:#fff;font-size:12px}
#mansi-theme-grid button[aria-pressed=true]{border-color:var(--mansi-accent,#258bff);background:#ffffff1b;box-shadow:0 0 12px color-mix(in srgb,var(--mansi-accent,#258bff) 35%,transparent)}
#mansi-theme-grid i{display:block;flex:0 0 20px;width:20px;height:20px;border-radius:50%;background:var(--swatch);box-shadow:0 0 10px var(--swatch)}
#mansi-theme-close{width:100%;margin-top:10px;border:0;border-radius:10px;padding:10px;background:var(--mansi-accent,#258bff);color:#07101e;font-weight:800}
</style>
<button id="mansi-theme-open" type="button" aria-expanded="false">🎨 Themes</button>
<section id="mansi-theme-panel" aria-label="MANSI AI Theme Studio">
 <h3>Theme Studio · 12 looks</h3><p>Choose a vibe. Your selection stays saved on this device.</p>
 <div id="mansi-theme-grid">
  <button data-theme="midnight" aria-pressed="false"><i style="--swatch:#258BFF"></i>1. Midnight Neon</button>
  <button data-theme="galaxy" aria-pressed="false"><i style="--swatch:#A855F7"></i>2. Galaxy Fusion</button>
  <button data-theme="silver" aria-pressed="false"><i style="--swatch:#AFC9E8"></i>3. Silver Frost</button>
  <button data-theme="aura" aria-pressed="false"><i style="--swatch:#FF8FB1"></i>4. Soft Aura</button>
  <button data-theme="emerald" aria-pressed="false"><i style="--swatch:#20D6A2"></i>5. Emerald Pulse</button>
  <button data-theme="ocean" aria-pressed="false"><i style="--swatch:#00CFE8"></i>6. Ocean Wave</button>
  <button data-theme="sunset" aria-pressed="false"><i style="--swatch:#FF7849"></i>7. Sunset Glow</button>
  <button data-theme="carbon" aria-pressed="false"><i style="--swatch:#D1D5DB"></i>8. Carbon Black</button>
  <button data-theme="champagne" aria-pressed="false"><i style="--swatch:#D8B477"></i>9. Champagne</button>
  <button data-theme="cyber" aria-pressed="false"><i style="--swatch:#4F6BFF"></i>10. Cyber Space</button>
  <button data-theme="lavender" aria-pressed="false"><i style="--swatch:#B9A2FF"></i>11. Lavender Mist</button>
  <button data-theme="mint" aria-pressed="false"><i style="--swatch:#67DCCB"></i>12. Arctic Mint</button>
 </div>
 <button id="mansi-theme-close" type="button">Done</button>
</section>
<script>
(function(){
 const themes={
  midnight:{accent:'#258BFF',bg:'#071329',surface:'#102747',text:'#EAF4FF'},
  galaxy:{accent:'#A855F7',bg:'#100824',surface:'#251344',text:'#F5ECFF'},
  silver:{accent:'#80BFFF',bg:'#EAF1F8',surface:'#FFFFFF',text:'#23364D'},
  aura:{accent:'#FF8FB1',bg:'#FFF0F3',surface:'#FFFFFF',text:'#572B43'},
  emerald:{accent:'#20D6A2',bg:'#061F1C',surface:'#103A34',text:'#E4FFF7'},
  ocean:{accent:'#00CFE8',bg:'#061B2B',surface:'#0D344A',text:'#E4FAFF'},
  sunset:{accent:'#FF7849',bg:'#2A111A',surface:'#4A2028',text:'#FFF0E9'},
  carbon:{accent:'#D1D5DB',bg:'#101113',surface:'#242629',text:'#F5F5F5'},
  champagne:{accent:'#D8B477',bg:'#F7F0E3',surface:'#FFFCF5',text:'#443723'},
  cyber:{accent:'#4F6BFF',bg:'#080B25',surface:'#171D48',text:'#EEF0FF'},
  lavender:{accent:'#B9A2FF',bg:'#F2EEFF',surface:'#FFFFFF',text:'#382D59'},
  mint:{accent:'#37BFAE',bg:'#E9FAF7',surface:'#FFFFFF',text:'#17453F'}
 };
 const key='mansi_theme_studio_v1',panel=document.getElementById('mansi-theme-panel'),opener=document.getElementById('mansi-theme-open'),grid=document.getElementById('mansi-theme-grid');
 if(!panel||!opener||!grid)return;
 function apply(name,save){
  const t=themes[name]||themes.midnight,root=document.documentElement;
  root.style.setProperty('--mansi-accent',t.accent);
  root.style.setProperty('--mansi-user-accent',t.accent);
  root.style.setProperty('--mansi-theme-bg',t.bg);
  root.style.setProperty('--mansi-theme-surface',t.surface);
  root.style.setProperty('--mansi-theme-text',t.text);
  document.body.style.setProperty('background-color',t.bg,'important');
  document.body.style.setProperty('color',t.text,'important');
  document.querySelectorAll('#heart-overlay,.heart-overlay,.orb-glow,.orb-core').forEach(function(el){
   el.style.setProperty('--mansi-accent',t.accent);
   if(el.id==='heart-overlay'||el.classList.contains('heart-overlay'))el.style.filter='drop-shadow(0 0 10px '+t.accent+') drop-shadow(0 0 22px '+t.accent+')';
  });
  grid.querySelectorAll('[data-theme]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.theme===name));});
  if(save){try{localStorage.setItem(key,name);}catch(e){}}
 }
 opener.addEventListener('click',function(){const open=!panel.classList.contains('open');panel.classList.toggle('open',open);opener.setAttribute('aria-expanded',String(open));});
 grid.addEventListener('click',function(e){const b=e.target.closest('[data-theme]');if(b)apply(b.dataset.theme,true);});
 document.getElementById('mansi-theme-close').addEventListener('click',function(){panel.classList.remove('open');opener.setAttribute('aria-expanded','false');});
 let saved='midnight';try{saved=localStorage.getItem(key)||'midnight';}catch(e){}apply(saved,false);
})();
</script>
"""
if "</body>" in html:
    html = html.replace("</body>", block + "\n</body>", 1)
elif "</html>" in html:
    html = html.replace("</html>", block + "\n</html>", 1)
else:
    html += "\n" + block
path.write_text(html, encoding="utf-8")
print("Added 12 selectable MANSI themes with saved selection and orb accent matching.")
