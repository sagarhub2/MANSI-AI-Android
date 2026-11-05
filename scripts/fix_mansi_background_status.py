from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.is_dir():
    raise SystemExit(f"MANSI background branding: missing source tree {ROOT}")

replacements = [
    (re.compile(r"(?i)\\bJarvis\\s+is\\s+in\\s+the\\s+background\\b"), "MANSI AI is running in the background"),
    (re.compile(r"(?i)\\bJarvis\\s+in\\s+the\\s+background\\b"), "MANSI AI running in the background"),
    (re.compile(r"(?i)\\bJarvis\\s+is\\s+running\\s+in\\s+the\\s+background\\b"), "MANSI AI is running in the background"),
    (re.compile(r"(?i)\\bJarvis\\s+is\\s+in\\s+background\\b"), "MANSI AI is running in the background"),
]

changed = []
for path in ROOT.rglob("*"):
    if path.suffix.lower() not in {".kt", ".java", ".xml", ".json", ".html", ".js", ".txt", ".properties"}:
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    after = before
    for pattern, replacement in replacements:
        after = pattern.sub(replacement, after)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(str(path))

print("MANSI background status branding updated:", *(changed or ["no matching legacy visible text found"]), sep="\\n  ")
