# Engineering Figure Agent

Engineering Figure Agent is not a general academic-figure platform. It is an agent-native skill for engineering and CS paper figures, designed to separate conceptual diagrams from exact quantitative plots.

## Positioning

This repository focuses on the figure-production layer inside an existing research workflow.

It is a good fit for:

- researchers who already know what figure they need
- Codex or agent users who want figure generation inside their research workflow
- users who need both method diagrams and exact quantitative plots
- authors in CS, systems, algorithms, electronics, and embedded domains

It is intentionally not centered on:

- a full paper-upload web app
- one-click end-to-end automation for every research task
- a broad all-discipline illustration platform

## Core Differentiation

### 1. Agent-native rather than platform-centric

- meant to be invoked from Codex workflows
- easy to compose with writing, coding, and experiment-analysis tasks
- emphasizes controllability over UI-heavy orchestration

### 2. Conceptual diagrams and quantitative plots use different pipelines

- `image mode`: system architecture, algorithm workflow, graphical abstract, engineering schematic
- `plot mode`: bar charts, trend curves, heatmaps, scatter plots, multi-panel publication figures

This is the key idea: paper figures should not be treated as a single generic prompt problem.

### 3. Optimized for engineering and CS papers

- system architecture
- algorithm workflow
- hardware block diagram
- benchmark / ablation / heatmap / scatter

### 4. Publication-oriented output quality

- white backgrounds
- compact, readable labels
- bilingual technical readability
- local exact plotting for numeric figures
- export-ready `png / pdf / svg`

## Recommended Workflow

The best workflow is usually:

1. Use `ai-research-writing-guide` to decide:
   - what claim the figure should support
   - what figure type is appropriate
   - what panel or module structure is required
   - what caption logic must be preserved
2. Use `engineering-figure-agent` to render the final figure

Recommended upstream handoff fields:

- figure goal
- figure type
- panel plan or module list
- must-keep terms
- output language
- visual constraints

## Optional Upstream Skill: ai-research-writing-guide

`ai-research-writing-guide` is a recommended upstream skill, not a hard dependency.

It is useful for:

- extracting a figure goal from paper text
- deciding what figure type best fits the claim
- drafting a panel plan or module plan
- preserving caption logic and must-keep terms

`engineering-figure-agent` works on its own.  
If you already know what figure you want to make, you can use this skill directly without installing the upstream one.

If you want a fuller workflow like:

`paper text -> figure brief -> final figure`

then it is worth installing `ai-research-writing-guide` as well.

Recommended install path:

- `$HOME/.codex/skills/ai-research-writing-guide`

For example:

```powershell
git clone https://github.com/Leey21/awesome-ai-research-writing $HOME/.codex/skills/ai-research-writing-guide
```

After installation, it is recommended to:

1. restart Codex
2. explicitly mention `ai-research-writing-guide` in chat
3. run one figure-brief or paragraph-analysis test

Example:

- `Use ai-research-writing-guide to turn this method section into a figure brief`

If Codex responds using the upstream writing/planning workflow, recognition is working.

### Third-Party Upstream Note

- `ai-research-writing-guide` is a recommended upstream skill
- its writing-side content is based on the third-party repository [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)
- this repository only documents the recommended workflow integration and does not claim ownership of the third-party project, nor guarantee its structure, availability, or future compatibility
- if you install the third-party repository directly, verify that its current structure is still compatible with Codex skill discovery

## Repository Layout

- `README.md`: bilingual landing page
- `README.zh-CN.md`: full Chinese guide
- `README.en.md`: full English guide
- `SKILL.md`: internal Codex skill instructions
- `scripts/`: setup, checks, prompt building, generation, and plotting
- `references/`: templates and publication-style references
- `examples/figure-briefs/`: reusable figure-brief starters
- `docs/examples/`: public showcase files and notes
- `providers.md`: provider-compatibility notes

## Two Modes

### `image mode`

Best for:

- system architecture diagrams
- algorithm workflows
- graphical abstracts
- electronics or embedded-system schematics
- reference-inspired redraws

Use this when visual structure matters more than exact numeric geometry.

Image mode can use the existing Gemini/Banana-compatible backend or the OpenAI Image API backend:

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --provider openai `
  --model gpt-image-1.5 `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

Use `OPENAI_API_KEY` or `OPENAI_API_KEY_FILE` for OpenAI. The original `NANOBANANA_*` configuration still controls the Gemini/Banana-compatible path.

### `plot mode`

Best for:

- benchmark bar charts
- ablation plots
- trend curves
- heatmaps
- scatter plots
- multi-panel result figures

Use this when exact values, axes, and geometry must stay correct.

Rule of thumb:

- if numeric truth matters, use `plot mode`
- if the figure is conceptual, use `image mode`
- if a figure mixes both, render the quantitative panels locally first and keep image generation for explanatory panels

## Platform Support

Windows is still the primary tested platform, but the core workflow is not limited to Windows.

- users have already reported successful installation and use on macOS
- some setups can be completed with AI-assisted installation rather than fully manual steps
- the core Python workflow usually works on Windows, macOS, and Linux
- the main caveat is that some helper scripts are still more Windows / PowerShell-oriented

The most portable parts of the repository are:

- `scripts/build_engineering_figure_prompt.py`
- `scripts/build_plot_spec.py`
- `scripts/plot_publication_figure.py`
- `scripts/generate_image.py`

For macOS / Linux users, the notes below are meant as a fallback guide and environment reference, not as the only supported path.

## Shortest Windows Install Path

If you want the shortest first-time setup path, run these PowerShell commands in order:

```powershell
git clone https://github.com/heyu-233/engineering-figure-agent $HOME/.codex/skills/engineering-figure-agent
Copy-Item $HOME/.codex/skills/engineering-figure-agent/secrets/nanobanana.env.example $HOME/.codex/secrets/nanobanana.env
Copy-Item $HOME/.codex/skills/engineering-figure-agent/secrets/nanobanana_api_key.txt.example $HOME/.codex/secrets/nanobanana_api_key.txt
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

Then:

1. edit `nanobanana.env` and `nanobanana_api_key.txt`
2. restart Codex
3. start your first generation test

## Restart Codex After First Install

This step is worth stating explicitly.

Why:

- Codex should rescan the skill directory after installation
- new local env and script changes are more reliable in a fresh session

Recommended sequence:

1. finish installation and secret configuration
2. close the current Codex session
3. reopen Codex
4. then verify the skill is recognized

## macOS / Linux Setup Notes

The core workflow can be used on macOS and Linux, and successful installs have already been reported.

In many cases, normal installation or AI-assisted setup is enough.  
If your environment still needs manual adjustment, the following steps are a reliable fallback:

```bash
git clone https://github.com/heyu-233/engineering-figure-agent ~/.codex/skills/engineering-figure-agent
mkdir -p ~/.codex/secrets
cp ~/.codex/skills/engineering-figure-agent/secrets/nanobanana.env.example ~/.codex/secrets/nanobanana.env
cp ~/.codex/skills/engineering-figure-agent/secrets/nanobanana_api_key.txt.example ~/.codex/secrets/nanobanana_api_key.txt
python3 -m pip install -r ~/.codex/skills/engineering-figure-agent/requirements.txt
```

Then:

1. edit `~/.codex/secrets/nanobanana.env`
2. replace the placeholder in `~/.codex/secrets/nanobanana_api_key.txt`
3. restart Codex
4. run a minimal Python script test

Example:

```bash
python3 ~/.codex/skills/engineering-figure-agent/scripts/generate_image.py \
  --figure-template system-architecture \
  --print-prompt \
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

If you prefer environment variables over a loader script, export them manually in your shell session or source them from your own shell config.

Typical reasons you might still need small manual adjustments:

- shell differences
- Python environment differences
- local proxy settings
- provider-specific API or auth settings

## Quick Start

### 1. Put the repo in the Codex skill directory

```powershell
$HOME/.codex/skills/engineering-figure-agent
```

### 2. Configure local secrets

Prepare these files outside the repo:

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

Templates are included here:

- `secrets/nanobanana.env.example`
- `secrets/nanobanana_api_key.txt.example`

### 3. Run setup and dependency checks

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

### 4. Load env vars

```powershell
. "$HOME/.codex/skills/engineering-figure-agent/scripts/load_nanobanana_env.ps1"
```

### 5. Run a minimal image test

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## Minimal Provider Templates

### Option 1: Official Gemini

`$HOME/.codex/secrets/nanobanana.env`

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
NANOBANANA_API_KEY_FILE=C:/Users/sly92/.codex/secrets/nanobanana_api_key.txt
```

`$HOME/.codex/secrets/nanobanana_api_key.txt`

```txt
REPLACE_WITH_YOUR_REAL_API_KEY
```

### Option 2: Gemini-compatible relay

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
NANOBANANA_API_KEY_FILE=C:/Users/sly92/.codex/secrets/nanobanana_api_key.txt
```

Advice:

- only enable `NANOBANANA_ALLOW_THIRD_PARTY=1` when you intentionally trust the relay
- for first verification, test the default path before trying high-resolution generation

## How To Verify Codex Recognizes The Skill

You can verify recognition in several ways:

### Method 1: Explicitly name the skill in chat

Examples:

- `Use engineering-figure-agent to create a system architecture prompt`
- `Use engineering-figure-agent to build a benchmark bar chart`

If Codex responds using the skill workflow, recognition is working.

### Method 2: Run the setup script

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

This helps you confirm:

- the skill path is correct
- the secrets exist
- required dependencies are available

### Method 3: Test the minimal prompt-building path

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --print-prompt `
  "A retrieval system with OCR, embedding, vector search, reranking, and answer synthesis."
```

If the final prompt prints correctly, the local script chain is already working.

## Common Failures And Fixes

### `python` not found

- make sure `python --version` works in PowerShell
- if not, install Python and add it to PATH

### API key file is still a placeholder

- open `$HOME/.codex/secrets/nanobanana_api_key.txt`
- replace the placeholder with a real key
- keep the file to one line only

### Third-party relay blocked by safety checks

- if you use a relay, add:
  - `NANOBANANA_ALLOW_THIRD_PARTY=1`
- otherwise the generator may refuse to send requests

### High-resolution request stops intentionally

- check whether `NANOBANANA_HIGHRES_MODEL` is configured
- verify that your provider actually exposes a high-resolution model
- do not expect silent fallback when high-res fails

### `load_nanobanana_env.ps1` says secrets are missing

- confirm these files exist:
  - `$HOME/.codex/secrets/nanobanana.env`
  - `$HOME/.codex/secrets/nanobanana_api_key.txt`

### Plotting scripts report missing dependencies

- run:

```powershell
pip install -r "$HOME/.codex/skills/engineering-figure-agent/requirements.txt"
```

## Example Gallery

The repository currently includes:

- autonomous-driving overview examples
- cooperative object tracking example
- multi-agent safety overview example
- Linux kernel system diagram example
- one supplementary health-monitoring deployment reference image

See:

- `docs/examples/README.md`

## Why Bilingual Docs Matter

This project benefits from bilingual documentation:

- GitHub discovery is more global and English-heavy
- social promotion in Chinese communities works better with Chinese docs
- the target audience includes both domestic graduate students and international agent / open-source users
- bilingual docs reduce friction and make repo sharing easier

Recommended doc strategy:

- `README.md`: bilingual landing page
- `README.zh-CN.md`: full Chinese guide
- `README.en.md`: full English guide
- gradually make key docs such as `providers.md` bilingual as well

## Project Summary

Engineering Figure Agent is an agent-native figure workflow for engineering and CS papers: image models for conceptual diagrams, local rendering for exact quantitative plots. It emphasizes controllable figure production, publication-oriented constraints, and exact quantitative rendering instead of treating every paper figure as the same generic image-generation problem.

## Notes

- never commit real API keys
- prefer local plotting for exact quantitative figures
- avoid hardcoding private relay endpoints in public docs unless they are clearly labeled as optional examples
