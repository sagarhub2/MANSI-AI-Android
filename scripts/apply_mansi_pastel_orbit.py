#!/usr/bin/env python3
"""Refresh the MANSI orb with soft pastel backdrop and fine orbital lines."""
from pathlib import Path
import re

root = Path("source/mansi/app/src/main")
asset = root / "assets/orb.html"
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "/* MANSI_CENTERED_HEART_ORBIT_V2 */"
if marker not in html:
    patch = r"""
<style>
/* MANSI_CENTERED_HEART_ORBIT_V2 — centered pastel halo, thin orbital lines */
#mansi-final-orb{
  position:fixed!important;left:50%!important;top:27.5%!important;
  transform:translate(-50%,-50%)!important;isolation:isolate!important;
  width:min(56vw,300px)!important;height:min(56vw,300px)!important;
  overflow:visible!important;background:transparent!important;border:0!important;
  box-shadow:none!important;filter:none!important
}
#mansi-final-orb::before{
  content:"";position:absolute;z-index:-2;left:50%;top:50%;
  width:178%;height:178%;transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(circle,rgba(255,105,222,.32) 0%,rgba(222,125,255,.23) 34%,rgba(184,150,255,.14) 56%,rgba(255,224,246,.07) 68%,transparent 74%);
  pointer-events:none;filter:blur(2px)
}
#mansi-final-orb::after{content:none!important;display:none!important}
#mansi-final-orb .mansi-ring{
  display:block!important;position:absolute!important;border-radius:50%!important;
  border:1.25px solid rgba(255,255,255,.88)!important;
  background:transparent!important;box-shadow:0 0 5px rgba(255,126,231,.28),0 0 12px rgba(213,128,255,.14)!important;
  z-index:1!important;opacity:1!important
}
#mansi-final-orb .mansi-ring:after{
  content:none!important;display:none!important
}
#mansi-final-orb .mansi-ring:before{
  content:"";position:absolute;width:9px;height:9px;left:50%;top:-5px;
  transform:translateX(-50%);border-radius:50%;
  background:#fffaff;box-shadow:0 0 7px 3px rgba(255,255,255,.88),0 0 15px 5px rgba(255,105,222,.6)
}
#mansi-final-orb .mansi-ring.r1{--inset:5%!important;--speed:19s!important;border-width:1.4px!important}
#mansi-final-orb .mansi-ring.r2{--inset:15%!important;--speed:26s!important;animation-direction:reverse!important;border-width:1.2px!important}
#mansi-final-orb .mansi-ring.r3{display:none!important}
#mansi-final-orb .mansi-core{
  position:absolute!important;inset:19%!important;z-index:2!important;border-radius:50%!important;
  background:radial-gradient(circle at 35% 28%,#fffaff 0%,#fff2fc 43%,#f9e1fb 76%,#f2d8fa 100%)!important;
  border:1px solid rgba(255,255,255,.88)!important;
  box-shadow:0 0 12px rgba(255,87,218,.5),0 0 30px rgba(255,62,211,.32),0 0 62px rgba(210,94,255,.2)!important
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
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="oval">
    <gradient
        android:type="radial"
        android:gradientRadius="180dp"
        android:startColor="#38FF70D9"
        android:centerColor="#20C28BFF"
        android:endColor="#00FFFFFF" />
</shape>
""", encoding="utf-8")
    print("Updated native orb halo to pink/lavender pastel.")
