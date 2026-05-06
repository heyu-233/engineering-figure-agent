---
name: engineering-figure-agent
description: Use when the user needs computer science, electronics, algorithms, or general engineering paper figures with Gemini or Nano Banana image models, or when they need exact publication-style plots rendered from numeric data. Prefer this skill for system architecture figures, algorithm workflows, pipeline diagrams, hardware block diagrams, circuit-level schematics, benchmark charts, ablation plots, scatter or heatmap panels, figure redrawing, and image editing through a Gemini-compatible endpoint.
---

# Engineering Figure Agent

## Overview

This skill adapts the Nano Banana or Gemini image workflow to computer science, electronics, algorithms, and engineering-paper figures.

## Boundary / Handoff

Use this skill for the figure-production layer after the figure goal is already reasonably clear.

- Good fit: turn a figure brief into a conceptual diagram, engineering schematic, workflow figure, or exact publication plot.
- Good fit: choose between `image` mode and `plot` mode, build prompts, render plots, and apply figure-language, layout, color, and export constraints.
- Not the main tool for: deciding from scratch what claim the paper should visualize, auditing whether a figure really supports the argument, or writing a full reviewer-style figure critique.
- If the user is still asking what figure they should make, what panels should exist, what claim each panel supports, or how the figure should be explained in the paper, hand off upstream to `ai-research-writing-guide` first.
- Recommended input from that upstream handoff: `figure goal`, `figure type`, `panel plan or module list`, `must-keep terms`, `caption or message`, `paper language`, and `visual style constraints`.

It should be treated as a provider-neutral workflow for image-generation backends:

- keep the official Google Gemini endpoint as the Banana/Gemini reference setup
- allow OpenAI Image API as a first-class image backend for conceptual figures and image edits
- allow third-party Gemini-compatible relays only when the user intentionally chooses them
- expect model names, auth mode, image-size options, and high-resolution options to vary by provider

Use two modes:

- `image` mode
  Use Gemini-compatible image generation or editing for conceptual figures, architecture diagrams, workflow schematics, graphical abstracts, and style-matched redraws.
- `plot` mode
  Use the bundled Python plotting tool for exact publication-style bar charts, trend curves, heatmaps, scatter plots, and multi-panel quantitative figures.

Rule of thumb:

- If numeric truth matters, use `plot` mode.
- If the figure is a conceptual schematic, use `image` mode.
- If a figure mixes both, render the quantitative plot locally first and use image generation only for the non-quantitative panels.
- Use `NANOBANANA_DEFAULT_MODEL` as the normal model for routine generation.
- Use `NANOBANANA_HIGHRES_MODEL` only when the user explicitly asks for higher resolution, final-export quality, or specifically mentions `2k`.
- Use `OPENAI_IMAGE_MODEL` when `--provider openai` is selected. The normal public default is `gpt-image-1.5`, but local configuration may override it.
- Use `OPENAI_IMAGE_HIGHRES_MODEL` for OpenAI only when a distinct final-quality or high-resolution model has been configured locally.
- The script now auto-selects `NANOBANANA_HIGHRES_MODEL` when the request clearly indicates high-resolution output, while keeping the normal default for routine runs.
- If a user clearly asks for `pro-2k`, 2K, higher-resolution, or final-export quality and that high-resolution path fails, stop immediately instead of silently falling back to a cheaper or lower-tier model.
- In that failure case, explicitly ask the human whether to retry the high-resolution request or to allow fallback. Do not make that downgrade decision automatically.
- If a user wants a specific provider model regardless of the auto-selection rules, a one-off `--model` override is still allowed.

## Quick Start

Set environment variables before image generation:

```bash
export NANOBANANA_API_KEY="your-provider-key"
export NANOBANANA_BASE_URL="https://generativelanguage.googleapis.com"
export NANOBANANA_MODEL="gemini-3.1-flash-image-preview"
```

## Local Secrets Bootstrap

This customized setup should prefer local secrets files over repeatedly hand-typing keys.

Default local files:

- `C:/Users/<user>/.codex/secrets/nanobanana.env`
- `C:/Users/<user>/.codex/secrets/nanobanana_api_key.txt`

Expected behavior:

1. If `NANOBANANA_*` variables are already present, use them directly.
2. If they are missing in the current shell, first load the local secrets files.
3. Only ask the user for the API key if the secrets files are missing or still contain placeholders.

PowerShell bootstrap in the same shell session:

```powershell
. "$HOME/.codex/skills/engineering-figure-agent/scripts/load_nanobanana_env.ps1"
```

After that, run the normal `generate_image.py` command in the same PowerShell session.

The local secrets files should contain:

- `nanobanana.env`
  - official Google example:
    - `NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com`
    - `NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview`
    - `NANOBANANA_AUTH_MODE=google`
  - third-party relay example:
    - `NANOBANANA_BASE_URL=https://your-relay.example.com`
    - `NANOBANANA_DEFAULT_MODEL=<your-default-image-model>`
    - `NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>`
    - `NANOBANANA_AUTH_MODE=bearer`
    - `NANOBANANA_ALLOW_THIRD_PARTY=1`
  - `NANOBANANA_API_KEY_FILE=.../nanobanana_api_key.txt`
- `nanobanana_api_key.txt`
  - one line containing the current valid API key

Do not store the real API key inside `SKILL.md`. Keep it only in the local key file.

For New API style relays that use `Authorization: Bearer ...`, also set:

```bash
export NANOBANANA_AUTH_MODE="bearer"
```

For OpenAI Image API generation, set:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_IMAGE_MODEL="gpt-image-1.5"
```

Then select the provider explicitly:

```bash
python3 scripts/generate_image.py \
  --provider openai \
  --figure-template system-architecture \
  --lang en \
  "A multimodal retrieval-augmented generation system with document ingestion, chunking, embedding, vector search, cross-encoder reranking, and final answer synthesis."
```

Recommended model configuration for this customized setup:

```bash
export NANOBANANA_DEFAULT_MODEL="<your-default-image-model>"
export NANOBANANA_HIGHRES_MODEL="<your-highres-image-model>"
```

Provider note:

- official Google and relay providers may use different model names
- do not assume a single public relay or reseller is the default
- for shared/public documentation, keep provider-specific endpoints as examples only

If you do not want the API key to appear in shell history, prefer:

```bash
export NANOBANANA_API_KEY_FILE="$PWD/.secrets/nanobanana_api_key"
```

Generate a conceptual engineering figure:

```bash
python3 scripts/generate_image.py \
  --figure-template system-architecture \
  --lang en \
  "A multimodal retrieval-augmented generation system with document ingestion, chunking, embedding, vector search, cross-encoder reranking, and final answer synthesis."
```

Build the prompt first without making any API call:

```bash
python3 scripts/build_engineering_figure_prompt.py \
  --figure-template algorithm-workflow \
  --lang en \
  --background-file ./method.md
```

Render an exact quantitative figure:

```bash
python3 scripts/build_plot_spec.py ./request.json --out ./spec.json
python3 scripts/plot_publication_figure.py ./spec.json --out-path ./output/plots/result --formats png pdf svg
```

## Workflow

1. Decide whether the user needs an exact plot or a conceptual figure.
2. For exact plots, read `references/publication-plot-api.md` and `references/natural-language-plot-workflow.md`, then render locally.
3. For conceptual figures, choose the closest template from `references/engineering-figure-templates.md`.
4. If layout fidelity matters, use a prompt-first workflow and inspect the resolved prompt before calling the API.
5. Keep labels short and explicit. Ask for a local file path only when the user needs exact image editing of an existing file.
6. Do not fabricate measurements, benchmark values, hardware specs, or unsupported causal claims.
7. Keep the normal default model for routine work, and use the configured high-resolution model only when the request clearly indicates 2K or final-export quality.
8. If `NANOBANANA_*` variables are missing, load `scripts/load_nanobanana_env.ps1` first, then run generation in the same shell session.
9. If the user wants ChatGPT/OpenAI-style image generation, use `--provider openai` and the `OPENAI_*` environment variables. Do not route OpenAI requests through Gemini relay settings.
10. If the user explicitly names a provider model, use a one-off `--model` override; otherwise let the script choose between the configured default and high-resolution model for the selected provider.
11. If a high-resolution request fails because of rate limits, network problems, upstream errors, or a missing high-resolution model setting, stop and ask the human what to do next. Never silently downgrade and burn tokens on a lower-tier model.

## Figure Templates

Use the built-in engineering templates instead of writing a long prompt from scratch when the request resembles:

- `graphical-abstract`
- `system-architecture`
- `algorithm-workflow`
- `electronic-schematic`

Prompt-building workflow:

1. Read `references/engineering-figure-templates.md`.
2. Select the closest template.
3. Choose `en` or `zh`. If the user does not specify a language and the technical background is mainly Chinese, default to `zh`; otherwise default to `en`.
4. Insert the user's technical background as-is.
5. Append journal or venue styling only after the base template.

## Plotting Guidance

Use `plot` mode for:

- benchmark bar charts
- learning curves
- ablation plots
- resource or latency tradeoff scatter plots
- confusion or attention heatmaps
- multi-panel result summaries

For natural-language plotting requests, infer the internal JSON spec yourself. Do not force the user to write the spec unless they explicitly ask for low-level control.

## Core Rules

- Favor white backgrounds, publication-style spacing, and short labels.
- Use blue for the main path or proposed method, green for beneficial outcomes, red for competing or failure paths, and neutral gray for background structure.
- Keep arrows, reading order, and module hierarchy explicit.
- Avoid decorative gradients, cinematic rendering, and unreadable micro-text.
- Treat image generation as concept rendering, not exact quantitative plotting.
- Prefer the official Google Gemini endpoint unless the user intentionally opts into a third-party compatible provider.
- If the provider is a relay such as New API, use `NANOBANANA_AUTH_MODE=bearer`.

## Journal Color Preference

When the user wants a journal-style figure, prefer a low-saturation, soft academic palette rather than bright infographic colors.

Recommended default palette from the user's preferred reference:

- main blue: `#92B1D9`
- light blue: `#C1D8E9`
- pale lavender: `#DBDDEF`
- soft peach: `#F6C8B6`
- light neutral gray: `#D4D4D4`

Suggested usage:

- Use `#92B1D9` for the primary method, main pathway, or key functional blocks.
- Use `#C1D8E9` for secondary modules, supporting flows, or background substructures.
- Use `#DBDDEF` for parallel branches, auxiliary stages, or soft emphasis regions.
- Use `#F6C8B6` for highlights, alerts, intervention modules, or contrast accents, but do not overuse it.
- Use `#D4D4D4` for non-focal infrastructure, containers, inactive regions, or neutral background elements.

Additional palette rules:

- Prefer low-to-medium saturation and avoid neon or overly vivid colors.
- Keep the total palette compact, usually 3-5 major colors in one figure.
- Preserve strong text-background contrast and avoid placing small text on dark or saturated fills.
- For publication figures, prioritize calm, clean, reviewer-friendly color balance over marketing-style visual impact.
- If the user provides a different venue style or brand palette, follow the user's request instead.

## Optional AutoFigure-Edit Handoff

If the user has a local deployment of [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit), this skill can optionally hand off a Banana-generated draft for downstream editable-figure refinement.

Use this handoff as an optional post-processing path, not as a guaranteed default step.

What AutoFigure-Edit is good at:

- generating editable `SVG` outputs for scientific figures
- refining structure, placeholders, and icon regions
- keeping a figure editable after draft generation

Important limitation:

- the current upstream AutoFigure-Edit workflow is primarily `method text -> draft figure -> editable SVG`
- it does support reference images and SVG reconstruction internally, but it does not currently expose a clean official one-flag CLI for `existing Banana raster image -> directly convert to editable SVG`
- so this skill should describe the integration as an optional local pipeline hook, not as a built-in guaranteed conversion path

Recommended handoff wording:

- If the user already has AutoFigure-Edit deployed locally, Banana can be used for the first-pass visual draft, and AutoFigure-Edit can be used afterward to reconstruct or refine an editable `SVG` version.
- Treat Banana as the draft-generation stage and AutoFigure-Edit as the editable-figure refinement stage.
- If the local AutoFigure-Edit workflow has been customized to accept an existing `figure.png`, prefer that path for post-processing.

Suggested local integration points to reserve:

- `AUTOFIGURE_EDIT_ROOT`: local repo root for AutoFigure-Edit
- `AUTOFIGURE_EDIT_PYTHON`: Python executable for that environment
- `AUTOFIGURE_EDIT_OUTPUT_DIR`: optional output directory for editable exports
- `AUTOFIGURE_EDIT_ENABLED=1`: optional local flag indicating that post-processing is available

Suggested artifact handoff:

- save the Banana raster draft as `figure.png`
- save the resolved prompt as `prompt.txt`
- save the scientific or technical background as `method.txt`
- optionally save a small `handoff.json` describing paths, language, figure type, and whether Chinese labels were requested

If this integration is mentioned in a response, phrase it conservatively:

- `This figure can optionally be handed off to a local AutoFigure-Edit deployment for editable SVG reconstruction or refinement if that pipeline is available on this machine.`
- `Direct Banana-image-to-editable-SVG conversion depends on the local AutoFigure-Edit setup and any custom wrapper scripts around the upstream project.`

## Chinese Text Guidance

If the requested figure contains Chinese text, apply practical readability rules because image models can blur, distort, or misalign dense Chinese labels. Support Chinese directly when the user wants it, but steer the prompt toward high legibility instead of over-restricting the design.

Use these rules:

- Chinese labels are allowed directly in the image and should be kept concise and legible; short labels are preferred, but moderate-length labels are acceptable when the user clearly needs them.
- Avoid paragraph-length Chinese text or dense multi-line explanation blocks inside the image unless the user explicitly requests a text-heavy figure.
- When the figure contains many Chinese labels, ask for larger label regions, stronger spacing, clear alignment, and higher contrast instead of defaulting to a text-free layout.
- For exact charts, prefer local plotting for accurate geometry; Chinese labels can be rendered directly when they remain readable at the intended export size.
- If the user explicitly wants Chinese directly inside the image, prioritize that requirement and optimize layout, font size, spacing, and label placement for readability.
- When the figure language is Chinese, preserve standard English symbols, formula variables, axis symbols, model names, protocol names, and established abbreviations where they improve technical clarity. Do not force awkward full-Chinese replacements for notation such as FFT, CNN, pH, loss, IoU, or variables like x, y, t, and sigma.
- If the user writes the figure request and paper context mainly in Chinese and does not explicitly force `en`, prefer Chinese labels by default.

When writing prompts for figures with Chinese, include prompt phrases like:

- `use concise, clear Chinese labels`
- `prefer short to medium Chinese labels`
- `avoid dense Chinese paragraph text`
- `preserve standard English symbols and formula variables where appropriate`
- `keep labels horizontally aligned and centered within boxes`
- `keep the figure readable at single-column paper width`
- `avoid dense annotation blocks`
- `white background, academic vector-like style, readable Chinese labels`
- `large clean text regions, centered Chinese labels, balanced spacing`
- `clear spacing, high contrast label areas, legible Chinese typography`

Safer prompt patterns:

- `Generate the full academic diagram structure with readable Chinese labels, balanced spacing, and clean alignment.`
- `Use concise Chinese module names and keep each label easy to read at paper size.`
- `Use Chinese for descriptive labels, but preserve standard English symbols, abbreviations, and formula variables where technically appropriate.`
- `Preserve the layout and arrows, and make the Chinese labels clear, centered, and visually balanced.`
- `For chart-like figures, emphasize accurate geometry and keep Chinese labels readable and uncluttered.`

## References

- `references/engineering-figure-templates.md`: template selection and domain-specific guidance.
- `references/publication-figure-design.md`: visual style rules for publication figures.
- `references/publication-chart-patterns.md`: chart composition and panel patterns.
- `references/natural-language-plot-workflow.md`: converting user requests into exact plotting specs.
- `references/publication-plot-api.md`: plot spec schema and rendering details.

## Scripts

- `scripts/build_engineering_figure_prompt.py`: resolve a template into a final prompt without any network call.
- `scripts/generate_image.py`: generate or edit images through the Gemini `generateContent` API shape.
- `scripts/build_plot_spec.py`: expand a concise plotting request into a complete plotting spec.
- `scripts/plot_publication_figure.py`: render exact figures from a JSON spec.
