from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.exists():
    raise SystemExit("Android source directory not found; refusing to continue.")

terms = (
    "notification", "notificationchannel", "notification_channel",
    "setcontenttitle", "setcontenttext", "contenttitle", "contenttext",
    "foregroundnotification", "channelname", "channel_name",
)
extensions = {".kt", ".java", ".xml", ".json", ".txt", ".html", ".js", ".properties"}
# Fix the exact notification phrases even when the line doesn't mention "notification".
phrase_patterns = (
    (re.compile(r"(?i)\bJarvis\s+is\s+ready\b"), "MANSI AI is ready"),
    (re.compile(r"(?i)\bhye\s+Jarvis\b"), "Hey MANSI"),
    (re.compile(r"(?i)\bHey\s+Jarvis\b"), "Hey MANSI"),
)

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in extensions:
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue

    after = before
    for pattern, replacement in phrase_patterns:
        after = pattern.sub(replacement, after)

    output = []
    for line in after.splitlines(keepends=True):
        normalized = line.lower().replace("-", "").replace(" ", "")
        if any(term in normalized for term in terms):
            line = re.sub(r"(?i)\bjarvis\b", "MANSI AI", line)
        output.append(line)
    after = "".join(output)

    if after != before:
        path.write_text(after, encoding="utf-8")
        print("Updated notification branding:", path)

print("Notification branding patch completed.")
