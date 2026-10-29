#!/usr/bin/env python3
"""Add native Android tap feedback to actionable MANSI XML views.

This runs against the unpacked project in CI so the change is applied to the
actual Android source used for the APK build, without replacing app behavior.
"""
from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main/res")
if not ROOT.exists():
    raise SystemExit("Android res directory not found; refusing to continue.")

ANDROID_FOREGROUND = 'android:foreground="?attr/selectableItemBackground"'
ANDROID_CLICKABLE = 'android:clickable="true"'
ANDROID_FOCUSABLE = 'android:focusable="true"'

# Common native widgets that should visibly respond to touch.
INTERACTIVE_TAGS = {
    "Button", "ImageButton", "ToggleButton", "Switch", "CheckBox", "RadioButton",
    "com.google.android.material.button.MaterialButton",
    "com.google.android.material.card.MaterialCardView",
    "androidx.cardview.widget.CardView",
}
# IDs commonly used for clickable cards, navigation items, and action rows.
INTERACTIVE_ID = re.compile(
    r"(?:^|[_-])(btn|button|action|profile|setting|settings|nav|navigation|"
    r"tab|menu|chat|voice|trigger|save|remove|send|mic|microphone|orb|"
    r"avatar|card|item|back|close|home|live|screen|permission|model)(?:$|[_-])",
    re.IGNORECASE,
)

changed = []
checked = 0
for path in ROOT.rglob("*.xml"):
    if "layout" not in path.parts and "menu" not in path.parts:
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue

    def add_attribute(tag, attribute):
        suffix = "/>" if tag.rstrip().endswith("/>") else ">"
        core = tag.rstrip()[:-len(suffix)].rstrip()
        return core + " " + attribute + " " + suffix

    def patch_tag(match):
        tag = match.group(0)
        tag_name_match = re.match(r"<([A-Za-z0-9_.$]+)", tag)
        if not tag_name_match:
            return tag
        tag_name = tag_name_match.group(1)
        attrs = dict(re.findall(r'([\w:.-]+)\s*=\s*"([^"]*)"', tag))
        view_id = attrs.get("android:id", "")
        is_interactive = (
            tag_name in INTERACTIVE_TAGS
            or attrs.get("android:clickable", "").lower() == "true"
            or attrs.get("android:onClick") is not None
            or bool(INTERACTIVE_ID.search(view_id.split("/")[-1]))
        )
        if not is_interactive:
            return tag
        updated = tag
        if "android:foreground=" not in updated:
            updated = add_attribute(updated, ANDROID_FOREGROUND)
        if 'android:clickable="true"' not in updated and tag_name not in INTERACTIVE_TAGS:
            updated = add_attribute(updated, ANDROID_CLICKABLE)
        if 'android:focusable="true"' not in updated:
            updated = add_attribute(updated, ANDROID_FOCUSABLE)
        return updated

    # Match only XML opening tags, preserving all unrelated source text.
    after = re.sub(r"<[A-Za-z][^<>]*>", patch_tag, before)
    checked += len(re.findall(r"<[A-Za-z][^<>]*>", before))
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(str(path))

print("MANSI tap-feedback patch: inspected", checked, "XML tags.")
print("Layouts/menu files updated:", len(changed))
for name in changed:
    print("  " + name)
