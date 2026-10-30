#!/usr/bin/env python3
"""Remove MANSI's center anime portrait and floating companion overlay."""
from pathlib import Path
import re

root = Path("source/mansi/app/src/main")
orb = root / "assets" / "orb.html"
if orb.exists():
    html = orb.read_text(encoding="utf-8")
    patch = r"""
<style id="MANSI_REMOVE_ANIME_AVATAR_V1">
#mansi-final-orb img.mansi-anime-avatar,
#mansi-final-orb .mansi-anime-avatar,
#mansi-final-orb .mansi-anime-art,
#mansi-final-orb .mansi-lips,
#mansi-final-orb .mansi-cheek,
#mansi-final-orb .mansi-eye-glint { display:none!important; visibility:hidden!important; }
</style>
<script>
(function(){
  function removePortrait(){
    var orb=document.getElementById('mansi-final-orb');
    if(!orb) return;
    orb.querySelectorAll('img.mansi-anime-avatar,.mansi-anime-avatar,.mansi-anime-art,.mansi-lips,.mansi-cheek,.mansi-eye-glint').forEach(function(n){n.remove();});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',removePortrait);
  else removePortrait();
  new MutationObserver(removePortrait).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>
"""
    if "MANSI_REMOVE_ANIME_AVATAR_V1" not in html:
        pos = html.lower().rfind("</body>")
        html = html[:pos] + patch + "\n" + html[pos:] if pos >= 0 else html + "\n" + patch
        orb.write_text(html, encoding="utf-8")
    print("Removed center anime portrait; retained the heart orb.")

manifest = root / "AndroidManifest.xml"
if manifest.exists():
    xml = manifest.read_text(encoding="utf-8")
    xml2 = re.sub(r'\s*<(?:activity|activity-alias)\b(?=[^>]*(?:OverlayAvatarActivity|overlay_avatar))[^>]*(?:/>|>.*?</(?:activity|activity-alias)>)', '', xml, flags=re.I | re.S)
    xml2 = re.sub(r'\s*<service\b(?=[^>]*(?:OverlayAvatar|FloatingAvatar|AvatarOverlay))[^>]*(?:/>|>.*?</service>)', '', xml2, flags=re.I | re.S)
    if xml2 != xml:
        manifest.write_text(xml2, encoding="utf-8")
    print("Removed floating-avatar activity/service manifest declarations where found.")

# Make the floating-avatar settings activity inert as a second safety measure.
for p in root.rglob("OverlayAvatarActivity.kt"):
    src = p.read_text(encoding="utf-8")
    if "MANSI_OVERLAY_DISABLED_V1" not in src:
        src2 = re.sub(
            r'(override\s+fun\s+onCreate\s*\([^)]*\)\s*\{)',
            r'\1\n        // MANSI_OVERLAY_DISABLED_V1\n        finish()\n        return',
            src, count=1
        )
        if src2 != src:
            p.write_text(src2, encoding="utf-8")
            print("Disabled overlay settings activity:", p)
print("MANSI avatar/overlay removal patch complete.")
