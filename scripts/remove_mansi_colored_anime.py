#!/usr/bin/env python3
"""Hide only the colored anime-girl portrait; preserve MANSI's pink heart orb."""
from pathlib import Path
import re

orb = Path("source/mansi/app/src/main/assets/orb.html")
if not orb.is_file():
    raise SystemExit(f"Required orb asset not found: {orb}")
html = orb.read_text(encoding="utf-8")
marker = "MANSI_REMOVE_COLORED_ANIME_KEEP_HEART_V1"
if marker not in html:
    patch = r"""
<style id="MANSI_REMOVE_COLORED_ANIME_KEEP_HEART_V1">
/* Remove the anime portrait only. Keep the orb, pink heart and its glow. */
#mansi-final-orb .mansi-anime-avatar,
#mansi-final-orb .mansi-anime-art,
#mansi-final-orb .mansi-avatar-face,
#mansi-final-orb .mansi-avatar-overlay {
  display:none!important;
  visibility:hidden!important;
}
</style>
"""
    pos = html.lower().rfind("</body>")
    html = html[:pos] + patch + "\n" + html[pos:] if pos >= 0 else html + "\n" + patch
    orb.write_text(html, encoding="utf-8")

# Match the approved clean mockup: keep one compact heart orb, remove the oversized
# halo/legacy circle layers, and clear the literal escaped newline placeholder.
clean_marker = "MANSI_CLEAN_HEART_HOME_V1"
if clean_marker not in html:
    clean_patch = r"""
<style id="MANSI_CLEAN_HEART_HOME_V1">
/* One compact soft-pink heart orb; no oversized halo or decorative circle. */
#mansi-final-orb { filter:none!important; background:transparent!important; box-shadow:none!important; }
#mansi-final-orb .mansi-core {
  background:radial-gradient(circle at 38% 30%,#fffaff 0%,#fff2fb 52%,#f8e0fa 100%)!important;
  border:0!important; outline:0!important;
  box-shadow:0 0 10px rgba(255,87,218,.30),0 0 22px rgba(255,62,211,.16)!important;
}
#mansi-final-orb .mansi-core::before,
#mansi-final-orb .mansi-core::after,
#mansi-final-orb::before,#mansi-final-orb::after { display:none!important; content:none!important; }
#mansi-final-orb .mansi-ring,
#mansi-final-orb .mansi-tapwave { display:none!important; visibility:hidden!important; }
</style>
<script>
(function(){
  function clean(){
    // Remove only the visibly broken literal "\\n \\n" placeholder text.
    var walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    var nodes=[],n;
    while((n=walker.nextNode())){
      if(/^(?:\\s*\\\\n\\s*){2,}$/.test(n.nodeValue||'')) nodes.push(n);
    }
    nodes.forEach(function(node){node.parentNode&&node.parentNode.removeChild(node);});
    // Remove leftover legacy orb/halo circles outside the active heart orb.
    document.querySelectorAll('[id*="orb" i],[class*="orb" i],[id*="heart" i],[class*="heart" i]').forEach(function(el){
      if(el.id==='mansi-final-orb'||el.closest('#mansi-final-orb')||el.contains(document.getElementById('mansi-final-orb'))) return;
      el.style.setProperty('display','none','important');
      el.setAttribute('aria-hidden','true');
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',clean); else clean();
  new MutationObserver(clean).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>
"""
    pos = html.lower().rfind("</body>")
    html = html[:pos] + clean_patch + "\n" + html[pos:] if pos >= 0 else html + "\n" + clean_patch
    orb.write_text(html, encoding="utf-8")
print("Cleaned oversized orb halo and stray literal newline text; kept the pink heart.")
