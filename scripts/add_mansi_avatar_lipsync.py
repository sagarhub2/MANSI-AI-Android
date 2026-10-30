#!/usr/bin/env python3
"""Add a face overlay, speaking mouth motion, gaze response and avatar theme hooks."""
from pathlib import Path
import re

asset = Path("source/mansi/app/src/main/assets/orb.html")
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "MANSI_AVATAR_FACE_LAYER_V1"
if marker in html:
    print("MANSI avatar face layer already installed.")
    raise SystemExit(0)

patch = r"""
<style>
/* MANSI_AVATAR_FACE_LAYER_V1 */
#mansi-final-orb .mansi-anime-avatar{
  position:absolute!important;left:50%!important;top:48%!important;
  width:48%!important;height:48%!important;transform:translate(-50%,-50%);
  overflow:visible;pointer-events:none;
  filter:drop-shadow(0 8px 14px rgba(91,49,133,.24));
}
#mansi-final-orb .mansi-anime-art{
  position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
  pointer-events:none;user-select:none;
}
#mansi-final-orb .mansi-lips{
  position:absolute;left:50%;top:62.8%;width:11%;height:2.2%;
  transform:translate(-50%,-50%);
  border-radius:0 0 50% 50%;
  background:linear-gradient(180deg,#d85c91,#a93c70);
  box-shadow:0 1px 1px rgba(255,255,255,.55);
  transform-origin:center center;
  transition:height 65ms ease, border-radius 65ms ease;
}
#mansi-final-orb.speaking .mansi-lips{
  height:var(--mansi-mouth-open,7%);
  border-radius:48%;
  animation:mansi-mouth-talk 150ms ease-in-out infinite alternate;
}
#mansi-final-orb.listening .mansi-lips{height:2.5%;opacity:.82}
#mansi-final-orb .mansi-cheek{
  position:absolute;top:58.4%;width:8%;height:3.5%;border-radius:50%;
  background:rgba(255,112,164,.24);filter:blur(2px);opacity:.5;
}
#mansi-final-orb .mansi-cheek.left{left:12%}
#mansi-final-orb .mansi-cheek.right{right:12%}
#mansi-final-orb .mansi-eye-glint{
  position:absolute;top:48%;width:2.8%;height:4%;border-radius:50%;
  background:rgba(255,255,255,.9);box-shadow:0 0 4px #fff;
  transition:transform .12s ease;
}
#mansi-final-orb .mansi-eye-glint.left{left:41%}
#mansi-final-orb .mansi-eye-glint.right{left:56%}
#mansi-final-orb .mansi-anime-avatar.mansi-surprised .mansi-lips{
  height:7%;width:6%;border-radius:50%;
}
#mansi-final-orb .mansi-anime-avatar.mansi-shy .mansi-cheek{opacity:1;background:rgba(255,83,151,.42)}
#mansi-final-orb .mansi-anime-avatar.mansi-sleepy .mansi-eye-glint{opacity:.35}
#mansi-final-orb .mansi-anime-avatar.mansi-happy .mansi-lips{height:2.8%;border-radius:0 0 50% 50%}
#mansi-final-orb .mansi-anime-avatar.mansi-3d{
  filter:drop-shadow(0 9px 15px rgba(91,49,133,.3)) drop-shadow(0 0 9px rgba(244,105,218,.22));
}
@keyframes mansi-mouth-talk{
  from{transform:translate(-50%,-50%) scaleY(.35)}
  to{transform:translate(-50%,-50%) scaleY(1.12)}
}
@media(prefers-reduced-motion:reduce){
  #mansi-final-orb .mansi-lips{animation:none!important;transition:none!important}
}
</style>
<script>
(function(){
 function installFace(){
   const orb=document.getElementById('mansi-final-orb');
   const image=orb && orb.querySelector('img.mansi-anime-avatar');
   if(!orb || !image || image.dataset.faceLayer==='1') return;
   const face=document.createElement('div');
   face.className='mansi-anime-avatar mansi-3d';
   image.classList.remove('mansi-anime-avatar');
   image.classList.add('mansi-anime-art');
   const syncMood=()=>['mansi-wink','mansi-happy','mansi-shy','mansi-surprised','mansi-sleepy'].forEach(c=>face.classList.toggle(c,image.classList.contains(c)));
   new MutationObserver(syncMood).observe(image,{attributes:true,attributeFilter:['class']});
   syncMood();
   image.dataset.faceLayer='1';
   image.parentNode.insertBefore(face,image);
   face.appendChild(image);
   ['left','right'].forEach(side=>{
     const cheek=document.createElement('i');cheek.className='mansi-cheek '+side;face.appendChild(cheek);
     const glint=document.createElement('i');glint.className='mansi-eye-glint '+side;face.appendChild(glint);
   });
   const lips=document.createElement('i');lips.className='mansi-lips';face.appendChild(lips);
   function gaze(x,y){
     const dx=Math.max(-2,Math.min(2,(x/window.innerWidth-.5)*4));
     const dy=Math.max(-1.5,Math.min(1.5,(y/window.innerHeight-.25)*2));
     face.querySelectorAll('.mansi-eye-glint').forEach(el=>el.style.transform='translate('+dx+'px,'+dy+'px)');
   }
   document.addEventListener('pointermove',e=>gaze(e.clientX,e.clientY),{passive:true});
   window.MANSIAvatarAudioLevel=function(level){
     const value=Math.max(0,Math.min(1,Number(level)||0));
     face.style.setProperty('--mansi-mouth-open',(2.2+value*8)+'%');
     if(value>.025) orb.classList.add('speaking');
   };
   window.MANSIAvatarSetTheme=function(theme){
     const palette={pink:['#ff70d5','#c95bff'],purple:['#b68cff','#745cff'],blue:['#69e5ff','#6587ff']};
     const colors=palette[String(theme).toLowerCase()]||palette.pink;
     face.style.setProperty('--mansi-avatar-glow',colors[0]);
     face.style.filter='drop-shadow(0 8px 15px '+colors[1]+'55) drop-shadow(0 0 9px '+colors[0]+'44)';
   };
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installFace);
 else installFace();
 const watch=new MutationObserver(installFace);
 watch.observe(document.documentElement,{childList:true,subtree:true});
})();
</script>
"""
if re.search(r"</body\s*>", html, re.I):
    html = re.sub(r"</body\s*>", patch + "\n</body>", html, count=1, flags=re.I)
else:
    html += "\n" + patch
asset.write_text(html, encoding="utf-8")
print("Installed face overlays, voice-state mouth animation, gaze response and pink/purple/blue theme hooks.")

# Build trigger: ensure this avatar enhancement is included in the next debug APK.
