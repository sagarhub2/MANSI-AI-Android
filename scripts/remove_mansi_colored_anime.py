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
print("Removed colored anime portrait only; pink heart orb remains.")
