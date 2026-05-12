# Figure Brief Spec

Engineering Figure Agent uses a figure brief as the platform-neutral input contract between paper thinking and figure production. Codex is the primary authoring environment, but the same brief can be used in Claude Code, ChatGPT, Claude, VS Code, Obsidian, or a future CLI.

## Required Fields

| Field | Type | Purpose |
|---|---|---|
| `figure_goal` | string | What this figure should help the paper prove or explain. |
| `paper_claim` | string | The claim, method contribution, or result the figure supports. |
| `figure_type` | string | `system-architecture`, `algorithm-workflow`, `graphical-abstract`, `electronic-schematic`, `benchmark-plot`, `mixed-panel`, or a domain-specific label. |
| `mode` | string | `image`, `plot`, or `mixed`. |
| `panels` | array | Panel/module plan, in reading order. |
| `must_keep_labels` | array | Terms that must remain faithful to the paper. |
| `data` | object | Numeric arrays, tables, links to data files, or `not_applicable`. |
| `style_constraints` | array | Venue, palette, language, density, aspect ratio, or export constraints. |
| `output_formats` | array | For example `png`, `pdf`, `svg`, or `prompt-only`. |
| `verification_checklist` | array | What must be checked before the figure is used in a paper. |

## Mode Rules

- Use `image` when the figure is conceptual, schematic, architectural, or reference-inspired.
- Use `plot` when numeric values, axes, error bars, or benchmark geometry must be exact.
- Use `mixed` when a figure combines local quantitative panels with conceptual panels.
- Do not invent numeric data. If numeric values are missing, ask for data or keep the figure conceptual.

## Minimal JSON Example

```json
{
  "figure_goal": "Explain the full RAG pipeline in one publication-style architecture figure.",
  "paper_claim": "The method improves answer reliability by separating retrieval, reranking, and synthesis.",
  "figure_type": "system-architecture",
  "mode": "image",
  "panels": [
    {
      "name": "Pipeline",
      "content": "Documents -> OCR -> chunks -> embeddings -> vector search -> reranking -> answer synthesis"
    }
  ],
  "must_keep_labels": ["OCR", "Embedding", "Vector Search", "Reranking", "Answer Synthesis"],
  "data": {"not_applicable": true},
  "style_constraints": ["white background", "short labels", "left-to-right flow", "English labels"],
  "output_formats": ["png"],
  "verification_checklist": [
    "All labels are readable at paper width.",
    "No unsupported numerical claims are shown.",
    "Data flow direction is unambiguous."
  ]
}
```

## Plot Request Relationship

For exact plots, the figure brief should point to or contain a `plot-request` object. The concise plot request is expanded by `scripts/build_plot_spec.py`, then rendered by `scripts/plot_publication_figure.py`.

The recommended multi-series scatter form is:

```json
{
  "kind": "scatter",
  "title": "Latency vs Accuracy",
  "xlabel": "Latency (ms)",
  "ylabel": "Accuracy",
  "data": {
    "series": [
      {"label": "Ours", "x": [24], "y": [0.93], "color": "blue_main"},
      {"label": "Baseline", "x": [39], "y": [0.83], "color": "red_strong"}
    ]
  }
}
```

Single-series scatter remains supported through `data.x` and `data.y`.
