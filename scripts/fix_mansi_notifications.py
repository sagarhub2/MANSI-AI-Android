from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.exists():
    raise SystemExit("Android source directory not found; refusing to continue.")

# Text-bearing source/resources where notification labels may be defined.
extensions = {".kt", ".java", ".xml", ".json", ".txt", ".html", ".js", ".properties"}
notification_terms = (
    "notification", "notificationchannel", "notification_channel",
    "setcontenttitle", "setcontenttext", "contenttitle", "contenttext",
    "foregroundnotification", "channelname", "channel_name",
    "startforeground", "notify(", "notificationmanager",
)
# Common user-visible phrases are fixed wherever they occur, even if the
# string/resource line itself doesn't mention notifications.
phrase_patterns = (
    (re.compile(r"(?i)\bJarvis\s+is\s+ready\b"), "MANSI AI is ready"),
    (re.compile(r"(?i)\bhye\s+Jarvis\b"), "Hey MANSI"),
    (re.compile(r"(?i)\bHey\s+Jarvis\b"), "Hey MANSI"),
)

updated_files = 0
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
        lower = line.lower()
        normalized = lower.replace("-", "").replace(" ", "")
        # Replace branding in notification construction and notification
        # resource lines. Avoid package/import declarations and identifiers.
        is_notification_line = any(term in normalized for term in notification_terms)
        is_package_or_import = bool(re.match(r"\s*(package|import)\s+", line))
        if is_notification_line and not is_package_or_import:
            line = re.sub(r"(?i)\bjarvis\b", "MANSI AI", line)
        output.append(line)

    after = "".join(output)
    if after != before:
        path.write_text(after, encoding="utf-8")
        updated_files += 1
        print("Updated MANSI notification branding:", path)

print(f"Notification branding patch completed; updated {updated_files} file(s).")
