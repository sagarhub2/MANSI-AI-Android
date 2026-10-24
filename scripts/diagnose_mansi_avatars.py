#!/usr/bin/env python3
"""Inspect avatar UI, data sources, resources, and overlay service in the unpacked app."""
from pathlib import Path
import re

root = Path("source/mansi/app/src/main")
if not root.is_dir():
    raise SystemExit(f"Android source tree missing: {root}")

terms = re.compile(r"avatar|overlay|floating.?companion|choose an avatar|pick the companion|dock.?edge", re.I)
exts = {".kt", ".java", ".xml", ".json", ".html"}
hits = 0
for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in exts:
        continue
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        continue
    matched = [(i, line.strip()) for i, line in enumerate(lines, 1) if terms.search(line)]
    if matched:
        print(f"\n--- {p} ---")
        for i, line in matched[:100]:
            print(f"{i}: {line[:350]}")
            hits += 1
print(f"\nAvatar/overlay source matches: {hits}")

print("\n--- Drawable/image assets possibly usable as avatars ---")
asset_root = root
assets = []
for p in asset_root.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".png", ".webp", ".jpg", ".jpeg", ".gif", ".xml", ".json", ".svg"}:
        if re.search(r"avatar|companion|character|mascot|orb|floating|profile", p.name, re.I):
            assets.append(p)
for p in assets[:200]:
    print(p)
print(f"Matching avatar-like assets: {len(assets)}")
