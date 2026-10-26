from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.exists():
    raise SystemExit("Android source directory not found; refusing to continue.")

# Never rewrite Kotlin/Java source wholesale: string templates and identifiers can
# contain $Jarvis/$Mansi references. Apply only narrow, exact prompt phrase fixes.
exact_replacements = [
    ("You are Jarvis, a helpful AI assistant.", "You are MANSI AI, Sagar's personal AI assistant. Your name is Mansi, never Jarvis. If asked your name or called Mansi, confirm warmly that you are Mansi AI. Speak naturally in casual Hinglish when the user does."),
    ("You are Jarvis.", "You are MANSI AI, Sagar's personal AI assistant. Your name is Mansi, never Jarvis."),
    ("I am Jarvis", "I am Mansi AI"),
    ("I'm Jarvis", "I'm Mansi AI"),
    ("My name is Jarvis", "My name is Mansi"),
    ("Mansi nahi Jarvis hu mein", "Main Mansi hoon, Jarvis nahi."),
    ("Mansi nahi, Jarvis hu mein", "Main Mansi hoon, Jarvis nahi."),
]
suffixes = {".kt", ".java", ".xml", ".json", ".txt", ".html", ".js", ".properties"}
changed = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in suffixes or path.name == "AndroidManifest.xml":
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    after = before
    # Restrict Kotlin/Java edits to lines that clearly define a prompt/identity.
    if path.suffix.lower() in {".kt", ".java"}:
        lines = after.splitlines(keepends=True)
        out = []
        for line in lines:
            low = line.lower()
            if any(marker in low for marker in ("prompt", "systeminstruction", "system instruction", "persona", "identity", "you are jarvis", "my name is jarvis")):
                for old, new in exact_replacements:
                    line = line.replace(old, new)
            out.append(line)
        after = "".join(out)
    else:
        for old, new in exact_replacements:
            after = after.replace(old, new)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(str(path))

print("Applied narrow MANSI identity phrase fixes without renaming Kotlin/Java identifiers.")
print("Files changed:", *changed, sep="\n  ")
