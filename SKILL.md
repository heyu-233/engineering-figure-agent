---
name: engineering-figure-agent
description: Use when the user needs computer science, electronics, algorithms, or general engineering paper figures with Gemini, Nano Banana, OpenAI image models, or exact publication-style plots rendered from numeric data. Prefer this skill for system architecture figures, algorithm workflows, pipeline diagrams, hardware block diagrams, circuit-level schematics, benchmark charts, ablation plots, scatter or heatmap panels, figure briefs, figure redrawing, image editing, and provider-neutral figure workflows.
---

# Engineering Figure Agent

Use this skill for the figure-production layer after the figure goal is reasonably clear.

## Boundary

Good fit:

- Turn a figure brief into a conceptual diagram, engineering schematic, workflow figure, or exact publication plot.
- Choose between `image`, `plot`, and `mixed` mode.
- Build prompts, render exact plots, and apply publication-style constraints.
- Refine existing prompts or figure briefs.

Not the main tool for:

- Deciding from scratch what claim a paper should visualize.
- Auditing whether a figure supports the paper argument.
- Writing full reviewer-style figure critique.

If the user is still deciding the figure claim, panel logic, or caption argument, use an available research-writing or paper-analysis skill upstream first.

## Core Decision

- `image` mode: conceptual figures, architecture diagrams, algorithm workflows, graphical abstracts, schematics, reference-inspired redraws.
- `plot` mode: exact bar charts, trend curves, heatmaps, scatter plots, ablation plots, benchmark summaries.
- `mixed` mode: render quantitative panels locally first, then use image generation only for conceptual panels.

Never use image generation for exact values, axes, or benchmark geometry.

## Default Workflow

1. Inspect the user input and decide whether a figure brief is already present.
2. If needed, create a brief using `docs/figure-brief-spec.md`.
3. Choose `image`, `plot`, or `mixed` mode.
4. For conceptual figures, prefer the prompt-builder scripts; read template references only when you need to inspect or customize template wording.
5. For exact plots, create a concise plot request and render it locally.
6. Keep labels short, claims source-grounded, and outputs publication-oriented.
7. Save prompt/spec/output paths when files are produced.
8. Before finishing, run only the checks needed for the touched path.

## Reference Loading

Read only what is needed:

- `references/engineering-figure-templates.md`: CS, electronics, algorithms, and engineering templates; read only when script output needs customization.
- `references/materials-science-figure-template.md`: materials-science figure templates; read only when script output needs customization.
- `references/publication-figure-design.md`: publication styling rules.
- `references/publication-chart-patterns.md`: plot and panel composition patterns.
- `references/natural-language-plot-workflow.md`: natural language to exact plot requests.
- `references/publication-plot-api.md`: full exact-plot spec.
- `references/provider-selection.md`: Gemini/Banana/OpenAI provider configuration.
- `references/highres-policy.md`: high-resolution and no-silent-downgrade rules.
- `references/chinese-labels.md`: Chinese label readability rules.
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
