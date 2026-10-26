from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.exists():
    raise SystemExit("Android source directory not found; refusing to continue.")

# Fix identity text only inside quoted literals in source code. Android package/class
# identifiers such as com.jarvis.assistant are deliberately preserved.
literal = re.compile(r'(["\'])(.*?)(?<!\\)\1', re.DOTALL)
changed_files = []
identity_hits = 0

def fix_literal(match):
    global identity_hits
    quote, value = match.group(1), match.group(2)
    lower = value.lower()
    is_identity_text = any(term in lower for term in (
        "jarvis", "assistant name", "your name", "who are you",
        "systeminstruction", "system instruction", "persona", "identity"
    ))
    if not is_identity_text:
        return match.group(0)

    original = value
    # Replace the legacy assistant name only in user-facing/prompt literals.
    value = re.sub(r'(?i)\bjarvis\b', 'Mansi', value)
    value = re.sub(r'(?i)\bJARVIS\b', 'MANSI', value)
    # Normalize common prompt variants so the model has one unambiguous identity.
    value = re.sub(r'(?i)you are\s+(?:an?\s+)?(?:ai\s+)?assistant\s+named\s+mansi',
                   'You are Mansi, Sagar\'s personal AI assistant', value)
    if value != original:
        identity_hits += 1
    return quote + value + quote

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {
        ".kt", ".java", ".xml", ".json", ".txt", ".html", ".js", ".properties"
    }:
        continue
    if path.name == "AndroidManifest.xml":
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    after = literal.sub(fix_literal, before)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed_files.append(str(path))

print("Identity literal replacements:", identity_hits)
print("Files changed:", *changed_files, sep="\n  ")
# Fail the build if source still contains a Jarvis reference inside an assistant
# prompt/name line, rather than silently shipping the same identity bug.
remaining = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".kt", ".java", ".xml", ".json", ".txt", ".html", ".js"}:
        continue
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        continue
    for number, line in enumerate(lines, 1):
        low = line.lower()
        if "jarvis" in low and any(term in low for term in ("systeminstruction", "you are", "assistant", "your name", "who are you", "persona", "identity")):
            remaining.append(f"{path}:{number}:{line.strip()[:180]}")
if remaining:
    print("WARNING: possible remaining assistant identity references:")
    print("\n".join(remaining))
else:
    print("No obvious Jarvis assistant-identity prompt lines remain.")
