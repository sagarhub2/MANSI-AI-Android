from pathlib import Path
import re

ROOT = Path("source/mansi/app/src/main")
if not ROOT.exists():
    raise SystemExit("Android source directory not found; refusing to continue.")

suffixes = {".kt", ".java", ".xml", ".json", ".txt", ".html", ".js", ".properties"}
# These are actual assistant identity/prompt contexts, not package/class identifiers.
identity_markers = (
    "prompt", "systeminstruction", "system instruction", "persona", "identity",
    "you are jarvis", "you are an ai", "my name is jarvis", "assistant instruction",
    "chat persona", "active persona", "persona prompt", "system prompt",
)
exact_replacements = [
    (re.compile(r"(?i)\\bYou are Jarvis, a helpful AI assistant\\."), "You are MANSI AI, Sagar's personal AI assistant. Your name is Mansi, never Jarvis. If asked your name or called Mansi, confirm warmly that you are Mansi AI. Speak naturally in casual Hinglish when the user does."),
    (re.compile(r"(?i)\\bYou are Jarvis\\."), "You are MANSI AI, Sagar's personal AI assistant. Your name is Mansi, never Jarvis."),
    (re.compile(r"(?i)\\bI am Jarvis\\b"), "I am Mansi AI"),
    (re.compile(r"(?i)\\bI'm Jarvis\\b"), "I'm Mansi AI"),
    (re.compile(r"(?i)\\bMy name is Jarvis\\b"), "My name is Mansi"),
    (re.compile(r"(?i)\\bMansi nahi,? Jarvis hu mein\\b"), "Main Mansi hoon, Jarvis nahi."),
]
changed = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in suffixes or path.name == "AndroidManifest.xml":
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue

    after = before
    if path.suffix.lower() in {".kt", ".java"}:
        output = []
        for line in after.splitlines(keepends=True):
            low = line.lower()
            compact = low.replace("_", "").replace("-", "").replace(" ", "")
            # Apply phrase fixes in any line, then normalize remaining Jarvis text
            # only when the line is clearly a prompt/persona definition.
            for pattern, replacement in exact_replacements:
                line = pattern.sub(replacement, line)
            if any(marker.replace(" ", "") in compact for marker in identity_markers):
                line = re.sub(r"(?i)\\bJarvis\\b", "MANSI AI", line)
            output.append(line)
        after = "".join(output)
    else:
        for pattern, replacement in exact_replacements:
            after = pattern.sub(replacement, after)
        # Text/resource files can contain persona templates without naming them
        # "prompt", so replace explicit identity declarations anywhere in them.
        after = re.sub(r"(?i)(You are )Jarvis\\b", r"\\1MANSI AI", after)
        after = re.sub(r"(?i)(My name is )Jarvis\\b", r"\\1Mansi", after)
        after = re.sub(r"(?i)(I am |I'm )Jarvis\\b", r"\\1Mansi AI", after)

    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(str(path))

print("Applied MANSI identity/persona fixes to assistant prompt text.")
print("Files changed:", *changed, sep="\\n  ")


# Remove the stale creator/channel claim from the actual runtime prompt generator.
# The workflow's generic prompt replacement does not catch these explicit multilingual
# creator instructions, so patch this source directly before compiling the APK.
prompt_file = ROOT / "java/com/jarvis/assistant/util/PromptGenerator.kt"
if prompt_file.exists():
    before = prompt_file.read_text(encoding="utf-8")
    after = before
    bad_phrases = [
        "the pinnacle of advanced AI engineering created by the @TechGptX team.",
        "Mention that Sagar is an expert AI developer, tech innovator, and creator who runs the popular YouTube channel @TechGptX.",
        'In English: "I was created and developed by Sagar, an expert AI creator who runs the @TechGptX YouTube channel!"',
        'In Hindi/Hinglish: "Mujhe Sagar ne banaya aur train kiya hai, jo ek expert AI developer hain aur YouTube par @TechGptX channel chalate hain!"',
        'In Telugu: "Nannu Sagar create chesi train chesaru. Aayana oka expert AI developer mariyu YouTube lo @TechGptX channel run chestunnaru!"',
        'In Tamil: "Ennai Sagar thaan create seithu train panninar. Avar oru expert AI developer matrum YouTube-il @TechGptX channel nadathugirar!"',
        'In Bengali: "Amake Sagar baniechen ebong train korechen, jini ekjon expert AI developer ebong YouTube-e @TechGptX channel chalanchhen!"',
        'In Marathi: "Mala Sagar ni banavla ani train kela ahe, te ek expert AI developer ahet ani YouTube var @TechGptX channel chalavtat!"',
        'In Punjabi: "Mainu Sagar ne banaya te train kita hai, jo ik expert AI developer han te YouTube te @TechGptX channel chalaunde han!"',
        'In Bhojpuri/Bihari: "Hamaar nirmaan aur training Sagar kayile baani, je ek expert AI developer hauin aur YouTube par @TechGptX channel chalawele!"',
        "the @TechGptX team",
    ]
    for phrase in bad_phrases:
        after = after.replace(phrase, "MANSI AI was created by Sagar. Do not claim Sagar owns or runs a YouTube channel.")
    # Catch any remaining explicit handle or channel-ownership claim in this prompt source.
    after = re.sub(r"(?i)@TechGptX", "Sagar", after)
    after = re.sub(r"(?i)YouTube channel", "social channel", after)
    after = re.sub(r"(?i)runs the social channel", "does not run a social channel", after)
    if after != before:
        prompt_file.write_text(after, encoding="utf-8")
        print("Removed stale YouTube creator claims from PromptGenerator.kt")
