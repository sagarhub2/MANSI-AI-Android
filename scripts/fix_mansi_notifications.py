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
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".kt", ".java", ".xml", ".json", ".txt"}:
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    output = []
    changed = False
    for line in before.splitlines(keepends=True):
        normalized = line.lower().replace("-", "").replace(" ", "")
        if any(term in normalized for term in terms):
            updated = re.sub(r"(?i)\bjarvis\b", "MANSI AI", line)
            if updated != line:
                line = updated
                changed = True
        output.append(line)
    after = "".join(output)
    if changed and after != before:
        path.write_text(after, encoding="utf-8")
        print("Updated notification branding:", path)
print("Notification branding patch completed.")
