#!/usr/bin/env python3
"""Refresh the MANSI orb with soft pastel backdrop and fine orbital lines."""
from pathlib import Path
import re

root = Path("source/mansi/app/src/main")
asset = root / "assets/orb.html"
if not asset.is_file():
    raise SystemExit(f"Required orb asset not found: {asset}")
html = asset.read_text(encoding="utf-8")
marker = "/* MANSI_PASTEL_ORBIT_REFRESH_V1 */"
if marker not in html:
    patch = r"""
<style>
/* MANSI_PASTEL_ORBIT_REFRESH_V1 — soft pastel halo + fine orbital lines */
#mansi-final-orb{isolation:isolate!important}
#mansi-final-orb::before{
  content:"";position:absolute;z-index:-2;left:50%;top:50%;
  width:190%;height:190%;transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(circle,rgba(255,91,218,.28) 0%,rgba(211,116,255,.20) 35%,rgba(177,149,255,.12) 56%,rgba(255,223,242,.05) 68%,transparent 74%);
  pointer-events:none;filter:blur(2px)
}
#mansi-final-orb::after{
  content:"";position:absolute;z-index:-1;left:50%;top:50%;
  width:142%;height:142%;transform:translate(-50%,-50%);border-radius:50%;
  border:1.5px solid rgba(255,184,239,.62);
  box-shadow:0 0 12px rgba(242,119,224,.16),inset 0 0 18px rgba(207,133,255,.08);
  pointer-events:none
}
#mansi-final-orb .mansi-ring{display:block!important;border:1px solid transparent!important;
  background:linear-gradient(transparent,transparent) padding-box,
  conic-gradient(from var(--angle,0deg),rgba(255,255,255,.9),rgba(255,125,222,.78),rgba(182,144,255,.6),rgba(255,255,255,.35),rgba(255,255,255,.9)) border-box!important;
  box-shadow:0 0 8px rgba(244,119,225,.18)!important;z-index:1!important}
#mansi-final-orb .mansi-ring:after{inset:-4px!important;border:1px solid rgba(255,211,247,.2)!important}
#mansi-final-orb .mansi-ring.r1{--inset:2%!important;--speed:24s!important;border-width:1.5px!important}
#mansi-final-orb .mansi-ring.r2{--inset:8%!important;--speed:18s!important;border-width:1px!important}
#mansi-final-orb .mansi-ring.r3{--inset:14%!important;--speed:32s!important;border-width:1px!important;opacity:.7}
#mansi-final-orb .mansi-core{z-index:2!important;background:radial-gradient(circle at 35% 28%,#fffaff 0%,#fff2fc 43%,#f9e1fb 76%,#f2d8fa 100%)!important;border:1px solid rgba(255,255,255,.88)!important;box-shadow:0 0 12px rgba(255,87,218,.5),0 0 30px rgba(255,62,211,.32),0 0 62px rgba(210,94,255,.2)!important}
#mansi-final-orb .mansi-heart{z-index:4!important}
#mansi-final-orb.idle .mansi-core{animation:mansi-soft-breathe 3.2s ease-in-out infinite!important}
@media(prefers-reduced-motion:reduce){#mansi-final-orb .mansi-ring{animation:none!important}}
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
