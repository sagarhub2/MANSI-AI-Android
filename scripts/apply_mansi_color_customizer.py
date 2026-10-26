from pathlib import Path

path = Path("source/mansi/app/src/main/assets/orb.html")
if not path.exists():
    raise SystemExit("orb.html missing; cannot apply MANSI color customizer safely.")
html = path.read_text(encoding="utf-8")
marker = "MANSI_COLOR_CUSTOMIZER_V1"
if marker in html:
    print("MANSI color customizer already present.")
    raise SystemExit(0)

block = r"""
<!-- MANSI_COLOR_CUSTOMIZER_V1: user-controlled persistent orb accent colors -->
<style>
#mansi-color-toggle{position:fixed;right:14px;top:14px;z-index:99999;width:42px;height:42px;border:1px solid #b9a4ff;border-radius:50%;color:#fff;background:rgba(23,15,48,.82);font-size:20px;box-shadow:0 0 16px var(--mansi-accent,#a855f7);backdrop-filter:blur(12px)}
#mansi-color-panel{position:fixed;right:14px;top:64px;z-index:99999;width:min(270px,calc(100vw - 36px));padding:14px;border:1px solid var(--mansi-accent,#a855f7);border-radius:18px;color:#fff;background:rgba(10,9,29,.94);box-shadow:0 0 24px color-mix(in srgb,var(--mansi-accent,#a855f7) 50%,transparent);font:14px system-ui,sans-serif;backdrop-filter:blur(16px);display:none}
#mansi-color-panel.open{display:block}
#mansi-color-panel .mansi-title{font-weight:800;letter-spacing:.08em;margin-bottom:10px}
#mansi-color-panel .mansi-presets{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
#mansi-color-panel .mansi-swatch{width:30px;height:30px;border-radius:50%;border:2px solid #ffffffaa;padding:0}
#mansi-color-panel label{display:block;margin:10px 0 5px;color:#ddd}
#mansi-color-panel input[type=color]{width:100%;height:38px;border:0;border-radius:10px;background:transparent}
#mansi-color-panel input[type=text]{box-sizing:border-box;width:100%;padding:9px;border-radius:9px;border:1px solid #6b5b91;background:#17132c;color:white}
#mansi-color-panel .mansi-actions{display:flex;gap:8px;margin-top:10px}
#mansi-color-panel .mansi-actions button{flex:1;border:0;border-radius:9px;padding:9px;color:white;background:#554080}
</style>
<button id="mansi-color-toggle" aria-label="Customize MANSI colors" title="Customize colors">🎨</button>
<section id="mansi-color-panel" aria-label="MANSI color customization">
 <div class="mansi-title">MANSI COLOR STUDIO</div>
 <div>Choose your glow colour</div>
 <div class="mansi-presets">
  <button class="mansi-swatch" data-color="#A855F7" style="background:#A855F7" aria-label="Purple"></button>
  <button class="mansi-swatch" data-color="#258BFF" style="background:#258BFF" aria-label="Blue"></button>
  <button class="mansi-swatch" data-color="#FF45C8" style="background:#FF45C8" aria-label="Pink"></button>
  <button class="mansi-swatch" data-color="#20D6A2" style="background:#20D6A2" aria-label="Emerald"></button>
  <button class="mansi-swatch" data-color="#FF7849" style="background:#FF7849" aria-label="Orange"></button>
  <button class="mansi-swatch" data-color="#FFFFFF" style="background:#FFFFFF" aria-label="White"></button>
 </div>
 <label for="mansi-color-picker">Custom colour</label>
 <input id="mansi-color-picker" type="color" value="#A855F7">
 <label for="mansi-color-hex">HEX code</label>
 <input id="mansi-color-hex" type="text" value="#A855F7" maxlength="7" spellcheck="false">
 <div class="mansi-actions"><button id="mansi-color-save">Save colour</button><button id="mansi-color-reset">Reset</button></div>
</section>
<script>
(function(){
 const key='mansi_user_orb_accent_v1';
 const panel=document.getElementById('mansi-color-panel');
 const picker=document.getElementById('mansi-color-picker');
 const hex=document.getElementById('mansi-color-hex');
 if(!panel||!picker||!hex)return;
 function valid(v){return /^#[0-9a-fA-F]{6}$/.test(v);}
 function apply(v,save){
  if(!valid(v))return;
  document.documentElement.style.setProperty('--mansi-accent',v);
  document.documentElement.style.setProperty('--mansi-user-accent',v);
  document.querySelectorAll('#heart-overlay, .heart-overlay, .orb-glow, .orb-core').forEach(function(el){
   el.style.setProperty('--mansi-accent',v);
   if(el.id==='heart-overlay'||el.classList.contains('heart-overlay'))el.style.filter='drop-shadow(0 0 10px '+v+') drop-shadow(0 0 22px '+v+')';
  });
  picker.value=v;hex.value=v.toUpperCase();
  if(save){try{localStorage.setItem(key,v.toUpperCase());}catch(e){}}
 }
 document.getElementById('mansi-color-toggle').addEventListener('click',function(){panel.classList.toggle('open');});
 document.querySelectorAll('#mansi-color-panel [data-color]').forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.color,true);});});
 picker.addEventListener('input',function(){apply(picker.value,true);});
 hex.addEventListener('change',function(){if(valid(hex.value.trim()))apply(hex.value.trim(),true);else hex.value=picker.value.toUpperCase();});
 document.getElementById('mansi-color-save').addEventListener('click',function(){if(valid(hex.value.trim()))apply(hex.value.trim(),true);else apply(picker.value,true);});
 document.getElementById('mansi-color-reset').addEventListener('click',function(){apply('#A855F7',true);});
 try{apply(localStorage.getItem(key)||'#A855F7',false);}catch(e){apply('#A855F7',false);}
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
print("Added persistent MANSI orb color picker, HEX input, presets, save/reset controls.")
