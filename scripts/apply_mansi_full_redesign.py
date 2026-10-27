#!/usr/bin/env python3
"""Apply the MANSI AI premium dark-glass visual refresh; no theme chooser."""
from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
RES = ROOT / "res"
VALUES = RES / "values"
if not ROOT.is_dir():
    raise SystemExit("Android source directory missing; refusing to apply redesign.")

palette = {
    "colorPrimary": "#536DFF", "colorPrimaryDark": "#080D1F",
    "colorAccent": "#A66BFF", "colorSecondary": "#A66BFF",
    "colorOnPrimary": "#FFFFFF", "colorOnSecondary": "#FFFFFF",
    "colorBackground": "#080D1F", "colorSurface": "#111A32",
    "colorOnBackground": "#F2F5FF", "colorOnSurface": "#F2F5FF",
    "colorSurfaceVariant": "#1B2746", "colorOutline": "#354568",
    "mansi_navy": "#080D1F", "mansi_surface": "#111A32",
    "mansi_surface_elevated": "#182443", "mansi_blue": "#536DFF",
    "mansi_violet": "#A66BFF", "mansi_pink": "#FF72D2",
    "mansi_text": "#F2F5FF", "mansi_muted": "#AAB6D3",
}
VALUES.mkdir(parents=True, exist_ok=True)

def patch_colors(path):
    raw = path.read_text(encoding="utf-8") if path.exists() else '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>\n'
    for name, value in palette.items():
        pat = re.compile(r'(<(?:color|item)\b[^>]*name=["\']' + re.escape(name) + r'["\'][^>]*>).*?(</(?:color|item)>)', re.S)
        raw, _ = pat.subn(lambda m: m.group(1) + value + m.group(2), raw, count=1)
    missing = [f'    <color name="{name}">{value}</color>' for name, value in palette.items()
               if not re.search(r'name=["\']' + re.escape(name) + r'["\']', raw)]
    if missing:
        raw = raw.replace("</resources>", "\n" + "\n".join(missing) + "\n</resources>", 1)
    path.write_text(raw, encoding="utf-8")

for p in VALUES.glob("colors*.xml"):
    patch_colors(p)
if not (VALUES / "colors.xml").exists():
    patch_colors(VALUES / "colors.xml")

drawable = RES / "drawable"
drawable.mkdir(parents=True, exist_ok=True)
(drawable / "mansi_app_background.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item><shape android:shape="rectangle">
        <gradient android:type="linear" android:angle="135" android:startColor="#080D1F" android:centerColor="#0C1430" android:endColor="#11102A"/>
    </shape></item>
</layer-list>
''', encoding="utf-8")
(drawable / "mansi_glass_surface.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <corners android:radius="22dp"/><solid android:color="#E6111A32"/>
    <stroke android:width="1dp" android:color="#333F68FF"/>
    <padding android:left="14dp" android:top="12dp" android:right="14dp" android:bottom="12dp"/>
</shape>
''', encoding="utf-8")

for p in list(VALUES.glob("themes*.xml")) + list(VALUES.glob("styles*.xml")):
    raw = p.read_text(encoding="utf-8")
    raw = re.sub(r'(<item\b[^>]*name=["\']android:windowBackground["\'][^>]*>).*?(</item>)',
                 r'\1@drawable/mansi_app_background\2', raw, flags=re.S)
    for key, value in {
        "android:statusBarColor": "#080D1F",
        "android:navigationBarColor": "#080D1F",
        "android:windowLightStatusBar": "false",
        "android:windowLightNavigationBar": "false",
        "android:colorAccent": "@color/colorAccent",
    }.items():
        pattern = re.compile(r'(<item\b[^>]*name=["\']' + re.escape(key) + r'["\'][^>]*>).*?(</item>)', re.S)
        if pattern.search(raw):
            raw = pattern.sub(lambda m: m.group(1) + value + m.group(2), raw, count=1)
        elif key not in ("android:windowLightStatusBar", "android:windowLightNavigationBar"):
            m = re.search(r'(<style\b[^>]*>)', raw)
            if m:
                raw = raw[:m.end()] + f'\n        <item name="{key}">{value}</item>' + raw[m.end():]
    p.write_text(raw, encoding="utf-8")

light = {"#FFFFFF":"#111A32", "#ffffff":"#111A32", "#FFF":"#111A32", "#fff":"#111A32",
         "#FAFAFA":"#111A32", "#fafafa":"#111A32", "#F5F5F5":"#182443", "#f5f5f5":"#182443",
         "#F8F9FA":"#111A32", "#f8f9fa":"#111A32"}
count = 0
layout_dir = RES / "layout"
for p in layout_dir.glob("*.xml") if layout_dir.exists() else []:
    raw = p.read_text(encoding="utf-8")
    updated = raw
    for old, new in light.items():
        updated = re.sub(r'(android:background=["\'])' + re.escape(old) + r'(["\'])',
                         lambda m: m.group(1) + new + m.group(2), updated)
    if updated != raw:
        p.write_text(updated, encoding="utf-8")
        count += 1

print("Applied single premium midnight / electric-blue / violet design system.")
print("Added gradient window background and reusable glass surface; retinted", count, "native layouts.")
print("No theme chooser or 12-theme UI added.")
