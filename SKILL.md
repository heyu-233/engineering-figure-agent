---
name: engineering-figure-agent
description: Use when the user needs engineering or research-paper figures: system architecture diagrams, algorithm workflows, hardware schematics, benchmark charts, ablation plots, figure briefs, redraws, image edits, or exact publication-style plots from numeric data. Covers Gemini, Nano Banana, OpenAI image models, and local plotting workflows.
---

# Engineering Figure Agent

Use this skill after the figure goal is already reasonably clear.

## Boundary

Good fit:

- Turn a figure brief into a conceptual diagram, workflow figure, schematic, or exact publication plot.
- Choose between `image`, `plot`, and `mixed` mode.
- Build prompts, render plots, and refine existing briefs.

Not the main tool for:

- Deciding from scratch what claim the paper should visualize.
- Full paper-argument or reviewer-style critique.

If the user is still deciding the figure claim, panel logic, or caption argument, use an available research-writing or paper-analysis skill upstream first.

## Core Decision

- `image` mode: conceptual figures, architecture diagrams, algorithm workflows, graphical abstracts, schematics, reference-inspired redraws.
- `plot` mode: exact bar charts, trend curves, heatmaps, scatter plots, ablation plots, benchmark summaries.
- `mixed` mode: render quantitative panels locally first, then use image generation only for conceptual panels.

Never use image generation for exact values, axes, or benchmark geometry.

## Default Workflow

1. Inspect the user input and decide whether a figure brief is already present.
2. If needed, create a brief using `references/figure-brief-spec.md`.
3. Choose `image`, `plot`, or `mixed` mode.
4. For conceptual figures, prefer the prompt-builder scripts; read template references only when you need to inspect or customize template wording.
5. For exact plots, create a concise plot request and render it locally.
6. Keep labels short, claims source-grounded, and outputs publication-oriented.
7. Save prompt/spec/output paths when files are produced.
8. Before finishing, run only the checks needed for the touched path.

## Reference Loading

Read only what is needed:

- `references/figure-brief-spec.md`: brief structure and mode rules.
- `references/publication-figure-design.md`: publication styling defaults.
- `references/provider-selection.md`: Gemini/Banana/OpenAI setup.
- `references/highres-policy.md`: high-resolution and fail-closed rules.
- `references/chinese-labels.md`: Chinese label readability rules.
- `references/engineering-figure-templates.md` and `references/materials-science-figure-template.md`: template wording when script output needs customization.
- `references/publication-chart-patterns.md`, `references/natural-language-plot-workflow.md`, and `references/publication-plot-api.md`: exact or plot-heavy workflows.
- `references/editable-figure-handoff.md`: optional editable SVG handoff.

## Scripts

- Build a prompt without network calls:

```bash
python scripts/build_engineering_figure_prompt.py --figure-template system-architecture --lang en "technical background"
python scripts/build_materials_figure_prompt.py --materials-figure mechanism-figure --lang en "scientific background"
```

- Generate or edit a conceptual image:

```bash
python scripts/generate_image.py --provider openai --figure-template system-architecture --lang en "technical background"
python scripts/generate_image.py --provider openai --materials-figure mechanism-figure --lang en "scientific background"
```

- Render an exact plot:

```bash
python scripts/build_plot_spec.py request.json --out spec.json
python scripts/plot_publication_figure.py spec.json --out-path output/figure --formats png pdf svg
```

- Use the unified CLI:

```bash
python scripts/efa.py prompt --figure-template system-architecture "technical background"
python scripts/efa.py prompt --materials-figure mechanism-figure "scientific background"
python scripts/efa.py plot request.json --out-path output/figure
python scripts/efa.py check
```

## Quality Rules

- Do not fabricate measurements, benchmark values, hardware specs, or unsupported causal claims.
- Keep arrows, reading order, and module hierarchy explicit.
- Favor white backgrounds, publication-style spacing, and readable labels.
- Use prompt-first workflows when layout fidelity matters.
- For high-resolution requests, follow `references/highres-policy.md`.
- For third-party providers, require explicit opt-in before sending keys or user files.
- For Chinese figures, preserve standard technical notation when it improves clarity.
