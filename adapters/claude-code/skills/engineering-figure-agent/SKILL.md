---
description: >
  Create engineering and CS paper figures from local paper context, method
  notes, code, data tables, or existing drafts. Use for figure briefs,
  conceptual diagrams, architecture figures, algorithm workflows, exact
  publication plots, prompt refinement, and light figure critique.
---

# Engineering Figure Agent For Claude Code

Use this skill for the figure-production layer after the figure goal is reasonably clear.

If the figure claim, panel logic, or caption argument is still unclear, first use a research-writing or paper-analysis workflow to settle the scientific message.

## Core Decision

- Use `image mode` for conceptual figures: system architecture, algorithm workflow, graphical abstract, hardware block diagram, or reference-inspired redraw.
- Use `plot mode` for exact values: benchmark bars, ablation plots, trend curves, heatmaps, scatter plots, or multi-panel quantitative figures.
- Use `mixed` when exact plot panels should be rendered locally and conceptual panels should be generated or described separately.

## Workflow

1. Inspect the user's paper context, data, caption draft, or figure brief.
2. Create or normalize a figure brief with `figure_goal`, `paper_claim`, `figure_type`, `mode`, `panels`, `must_keep_labels`, `data`, `style_constraints`, `output_formats`, and `verification_checklist`.
3. If numeric truth matters and data is missing, ask for values instead of inventing them.
4. For image mode, produce a final prompt using concise labels, white background, publication style, and faithful technical terms.
5. For plot mode, produce a concise plot-request JSON. Use `data.series[]` for multi-series scatter plots, and use outside or dedicated legends for dense annotated charts.
6. Keep real API keys outside the repository.
7. Require explicit user opt-in before sending API keys, prompts, or files to third-party provider endpoints.
8. For high-resolution or final-export requests, fail closed if the configured high-resolution path is unavailable instead of silently downgrading.
9. Treat generated diagrams as drafts until labels, scientific claims, and numeric values are verified.

## Output Files

Prefer these files when writing to disk:

```text
figure-brief.md
prompt.txt
plot-request.json
output/
```

## Quality Rules

- Do not fabricate measurements, benchmark improvements, device values, or unsupported causal claims.
- Keep labels readable at paper width.
- Preserve standard English symbols and formulas in Chinese figures when they improve clarity.
- Never use image generation for exact numeric chart geometry.
- Do not present light figure critique as a full reviewer-style paper-figure audit.
