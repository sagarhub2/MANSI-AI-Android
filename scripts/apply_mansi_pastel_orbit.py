#!/usr/bin/env python3
"""Refresh the MANSI orb with soft pastel backdrop and fine orbital lines."""
from pathlib import Path
import re

root = Path("source/mansi/app/src/main")
asset = root / "assets/orb.html"
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "/* MANSI_CENTERED_HEART_ORBIT_V5 */"
if marker not in html:
    patch = r"""
<style>
/* MANSI_CENTERED_HEART_ORBIT_V5 — lock the complete orb to the screen center */
#mansi-final-orb{
  position:fixed!important;left:50vw!important;top:41vh!important;
  transform:translate(-50%,-50%)!important;transform-origin:center center!important;
  width:min(56vw,300px)!important;height:min(56vw,300px)!important;aspect-ratio:1/1!important;
  margin:0!important;isolation:isolate!important;overflow:visible!important;
  background:transparent!important;border:0!important;box-shadow:none!important;filter:none!important;
  right:auto!important;bottom:auto!important
}
#mansi-final-orb::before{
  content:"";position:absolute!important;z-index:0!important;left:50%!important;top:50%!important;margin:0!important;
  width:172%!important;height:172%!important;
  transform:translate(-50%,-50%)!important;transform-origin:center center!important;border-radius:50%!important;
  background:radial-gradient(circle,rgba(255,94,218,.30) 0%,rgba(218,124,255,.22) 36%,rgba(185,145,255,.13) 57%,rgba(255,224,246,.055) 70%,transparent 74%)!important;
  pointer-events:none!important;filter:blur(1px)!important
}
#mansi-final-orb::after{content:none!important;display:none!important}
#mansi-final-orb .mansi-ring{
  display:block!important;position:absolute!important;border-radius:50%!important;
  border:1.25px solid rgba(255,255,255,.92)!important;background:transparent!important;
  box-shadow:0 0 5px rgba(255,126,231,.32),0 0 12px rgba(213,128,255,.18)!important;
  z-index:2!important;opacity:1!important;pointer-events:none!important
}
#mansi-final-orb .mansi-ring:after{content:none!important;display:none!important}
#mansi-final-orb .mansi-ring:before{
  content:"";position:absolute;width:8px;height:8px;left:50%;top:-4px;
  transform:translateX(-50%);border-radius:50%;background:#fffaff;
  box-shadow:0 0 7px 3px rgba(255,255,255,.9),0 0 15px 5px rgba(255,105,222,.58)
}
#mansi-final-orb .mansi-ring.r1{--inset:5%!important;--speed:19s!important;border-width:1.4px!important}
#mansi-final-orb .mansi-ring.r2{--inset:15%!important;--speed:26s!important;animation-direction:reverse!important;border-width:1.2px!important}
#mansi-final-orb .mansi-ring.r3{display:none!important}
#mansi-final-orb .mansi-core{
  position:absolute!important;inset:19%!important;z-index:3!important;border-radius:50%!important;
  background:radial-gradient(circle at 35% 28%,#fffaff 0%,#fff2fc 43%,#f9e1fb 76%,#f2d8fa 100%)!important;
  border:1px solid rgba(255,255,255,.9)!important;
  box-shadow:0 0 12px rgba(255,87,218,.46),0 0 28px rgba(255,62,211,.27),0 0 52px rgba(210,94,255,.17)!important
}
#mansi-final-orb .mansi-heart{z-index:4!important;width:18%!important;height:18%!important;left:50%!important;top:50%!important}
#mansi-final-orb .mansi-heart path{fill:#f45acb!important;stroke:#ffb5ee!important;stroke-width:1!important}
#mansi-final-orb.idle .mansi-core{animation:mansi-soft-breathe 3.2s ease-in-out infinite!important}
@media(prefers-reduced-motion:reduce){#mansi-final-orb .mansi-ring,#mansi-final-orb .mansi-core{animation:none!important}}
</style>
"""
    if re.search(r"</body\s*>", html, re.I):
        html = re.sub(r"</body\s*>", patch + "\n</body>", html, count=1, flags=re.I)
    else:
        html += "\n" + patch
    asset.write_text(html, encoding="utf-8")
    print("Applied pastel orbital linework to", asset)
else:
    print("Pastel orbital refresh already present.")

halo = root / "res/drawable/bg_jarvis_orb_halo.xml"
if halo.is_file():
    halo.write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="#00000000" />
</shape>
""", encoding="utf-8")
    print("Updated native orb halo to pink/lavender pastel.")
