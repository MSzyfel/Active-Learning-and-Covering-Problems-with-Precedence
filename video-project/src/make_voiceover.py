"""Generate scratch narration clips with an installed Windows speech voice."""

from pathlib import Path
import re
import sys

try:
    import pyttsx3
except ImportError:
    raise SystemExit("Install project dependencies first: python -m pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "script" / "voiceover.txt"
OUTPUT = ROOT / "output" / "voiceover"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    text = SCRIPT.read_text(encoding="utf-8")
    chapters = re.findall(r"CHAPTER\s+(\d+)\s*\n(.*?)(?=\nCHAPTER\s+\d+\s*\n|\Z)", text, re.S)
    if not chapters:
        raise SystemExit("No CHAPTER blocks found in script/voiceover.txt")
    try:
        engine = pyttsx3.init()
    except Exception as error:
        raise SystemExit(
            "No usable Windows SAPI speech voice is available in this session. "
            "Install/enable an English Windows speech voice, then run this script again. "
            f"Details: {error}"
        ) from None
    engine.setProperty("rate", 158)
    voices = engine.getProperty("voices")
    english = next((v.id for v in voices if re.search(r"en[-_]|english", f"{v.id} {v.name}", re.I)), None)
    if english:
        engine.setProperty("voice", english)
    for number, narration in chapters:
        path = OUTPUT / f"chapter_{int(number):02d}.wav"
        engine.save_to_file(narration.strip(), str(path))
        engine.runAndWait()
        print(path)
    engine.stop()


if __name__ == "__main__":
    main()
