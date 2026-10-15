# Precedence-Constrained Decision Trees: Video Proof of Concept

This project turns the paper into a narrated, animated technical talk. It uses **ManimGL**, Grant Sanderson's original open-source Manim project used for 3Blue1Brown-style explanations: <https://github.com/3b1b/manim>.

## Project contents

- `requirements/stoc2027-video-instructions.pdf` — the STOC 2027 author video requirements.
- `script/scenario.md` — full speaking script, storyboard, and timing plan.
- `script/voiceover.txt` — narration text, divided into chapters for optional synthetic narration.
- `src/video.py` — ManimGL animation with proof-step scenes and LaTeX-rendered mathematics.
- `src/make_voiceover.py` — optional offline Windows voice generation via `pyttsx3`/SAPI.
- `render.ps1` — configures project-local caches and bundled FFmpeg, then renders.
- `output/` — generated narration and rendered video.

The proof of concept compares three tests on the same twelve-hypothesis pool, uses an eight-outcome decision tree with mixed path depths, and shows a richer precedence DAG with multiple valid orders. The sepcover tree gives exact component counts. Its PDS graph is a seeded draw from the stated two-density model; planted vertices and edges are sampled rather than drawn as a guaranteed clique. The reduction calculations are split into separate cards. The Label Cover section shows its local-expander walk, bundle/witness dependencies, and heavy/light soundness bounds. Examples are labeled as illustrative when they are not theorem instances. All mathematical expressions in the video are rendered by LaTeX through ManimGL's `Tex` object. The chapter narration is also shown in a reserved caption band, so the silent render remains followable.

The local Windows SAPI voice engine denied access to its installed voices in this environment, so no scratch narration is included. The scene automatically uses chapter WAVs placed in `output/voiceover/` when they are available.

To add your own recording, export ten WAV clips named `chapter_01.wav` through `chapter_10.wav` into `output/voiceover/`, matching the chapter breaks in `script/scenario.md`. The renderer embeds each clip and uses its measured duration for that chapter. The STOC instructions require an author to present on camera; the generated animation is intended to accompany that recording.

## Setup (Windows PowerShell)

Install FFmpeg and a LaTeX distribution first. Then, from this directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src\make_voiceover.py
.\render.ps1 -LowQuality -Preview
.\render.ps1
```

The project targets the original `manimgl` package (Python 3.10+), not Manim Community Edition. ManimGL needs FFmpeg, OpenGL, and a LaTeX distribution for the rendered formulas. Consult the upstream README for platform-specific setup.

If no usable Windows speech voice is installed, the video still renders silently and the script remains the voice track to record. The current work environment did not expose a working Windows speech voice, so no audio file is included yet. The generator creates a clearly synthetic scratch narration when run on a configured machine; replace it with an author-recorded voice for any actual STOC submission.

## Render settings and outputs

The render is written beneath `output/manim/videos/`. The scene is designed for a 16:9 frame and uses the voice WAV files in `output/voiceover/` when available. Without them it follows the chapter time estimates in the scene. `render.ps1 -LowQuality -Preview` renders the opening animations as a quick setup check. `-FPS 12` makes a faster review render; omit `-LowQuality` for the default resolution.

The 3,405-word script targets about 20–22 minutes at a brisk but clear 155–165 words per minute. A slower author delivery will run closer to 24–27 minutes, still within the required range. Review chapter timing after recording; proofs and transitions may need more breathing room.

## Accuracy and use

The narration follows the submitted article's current claims and notation. It is a presentation draft, not a replacement for the paper. The accompanying instructions specify an author-presented video, so this generated voice is only for story, pacing, and visual proof-of-concept work.
