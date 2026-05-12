# Engineering Figure Agent

<div align="center">

![License](https://img.shields.io/badge/license-MIT-2563eb)
![Codex Skill](https://img.shields.io/badge/Codex-skill-111827)
![Figure Modes](https://img.shields.io/badge/modes-image%20%7C%20plot-f59e0b)
![Backends](https://img.shields.io/badge/backends-Gemini%20%7C%20OpenAI%20%7C%20local%20plots-16a34a)
![Focus](https://img.shields.io/badge/focus-engineering%20papers-7c3aed)

**Agent-native figure production for engineering and CS papers.**

把工程论文里的系统架构图、算法流程图、实验曲线和多面板图，拆成可控的生成流程：概念图走 image mode，精确数值图走 plot mode。

[中文说明](./README.zh-CN.md) | [English Guide](./README.en.md) | [Example Gallery](./docs/examples/README.md) | [Showcase](./docs/showcase.md)

</div>

## Preview

| System / Architecture | Cooperative Perception | Safety Taxonomy |
|---|---|---|
| ![Federated open-vocabulary driving figure](docs/examples/federated-open-vocab-driving-2k-1.png) | ![Cooperative object tracking figure](docs/examples/cooperative-object-tracking-2k-1.png) | ![Multi-agent safety overview figure](docs/examples/multi-agent-safety-overview-2k-1.png) |

| Dense Systems Diagram | Deployment Scenario |
|---|---|
| ![Linux kernel system diagram](docs/examples/linux-kernel-system-1.jpg) | ![Health monitoring and early warning deployment scenarios](docs/examples/health-monitoring-early-warning-reference.jpg) |

| Exact Local Plot |
|---|
| ![Benchmark plot](docs/examples/benchmark-plot.png) |

## Why It Exists

Most figure tools treat every paper figure as the same image prompt problem. Engineering papers do not work that way.

| Figure need | Better path |
|---|---|
| System architecture, pipeline, schematic, graphical abstract | `image mode` with an engineering-aware prompt template |
| Benchmark curves, ablation bars, heatmaps, scatter plots | `plot mode` with local plotting and exact values |
| Mixed conceptual + quantitative figure | Render numeric panels locally, then compose or describe the conceptual panels |
| Reference-inspired redraw | Use image mode for structure and style exploration, then manually verify labels and layout |

Engineering Figure Agent is intentionally lighter than a full paper-upload platform. It is built for researchers who already know what claim a figure should support and want a cleaner production path inside an agent workflow.

## Quick Start

Install and run the setup check:

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
```

Open the wizard:

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/wizard.ps1"
```

Or generate a conceptual figure directly:

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

For installation details, use the language-specific guides:

- [README.zh-CN.md](./README.zh-CN.md): Windows 最短安装路径、验证方法、中文示例
- [README.en.md](./README.en.md): setup, verification, examples, positioning

## Two Modes

### Image Mode

Use `image mode` when visual structure matters more than exact numeric geometry.

Best for:

- system architecture diagrams
- algorithm workflows
- graphical abstracts
- electronics or embedded-system schematics
- reference-inspired redraws and layout exploration

Supported conceptual-image backends:

| Provider | Use case | Config |
|---|---|---|
| `gemini` / `banana` | Google Gemini / Banana-compatible generation | `NANOBANANA_*` variables |
| `openai` | OpenAI Image API backend for conceptual figures and edits | `OPENAI_API_KEY` or `OPENAI_API_KEY_FILE` |

Example:

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --provider openai `
  --model gpt-image-1.5 `
  --figure-template system-architecture `
  --lang en `
  --openai-quality auto `
  --openai-size auto `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

### Plot Mode

Use `plot mode` when values, axes, and geometry must stay exact.

Best for:

- benchmark bar charts
- ablation plots
- trend curves
- heatmaps
- scatter plots
- multi-panel quantitative figures

Rule of thumb:

| If the figure needs... | Use |
|---|---|
| exact values, axes, error bars, or benchmark geometry | `plot mode` |
| concept explanation, layout exploration, or architecture visuals | `image mode` |
| both | local plot panels first, image generation only for conceptual parts |

## Workflow

Recommended upstream handoff:

1. Use `ai-research-writing-guide` to decide what claim the figure should support.
2. Write or collect the figure brief: audience, claim, modules, labels, data, and target style.
3. Use `engineering-figure-agent` to render the diagram or exact plot.
4. Verify labels, numeric truth, publication style, and export format before paper submission.

## Platform Adapters

| Platform | Entry | Best use |
|---|---|---|
| Codex | [SKILL.md](./SKILL.md) | Full agent-native workflow with local scripts |
| Claude Code | [adapters/claude-code/](./adapters/claude-code/) | Local repository figure work and prompt/plot generation |
| ChatGPT / Claude web | [docs/prompt-pack.md](./docs/prompt-pack.md) | Chat-only figure brief and prompt drafting |
| VS Code / Obsidian | [templates/figure-brief/](./templates/figure-brief/) | Edit and archive figure briefs, prompts, and plot requests |

Core platform-neutral contracts:

- [Figure brief spec](./docs/figure-brief-spec.md)
- [Plot request schema](./schemas/plot-request.schema.json)
- [Figure brief schema](./schemas/figure-brief.schema.json)

## Support Matrix

| Platform | Status | Notes |
|---|---|---|
| Windows | tested | primary tested platform; helper scripts supported first |
| macOS | reported working | successful installs have been reported, including AI-assisted setup |
| Linux | expected for core Python workflow | some environments may need small manual adjustments |

## Repository Map

| Path | Purpose |
|---|---|
| [SKILL.md](./SKILL.md) | Internal Codex skill instructions |
| [providers.md](./providers.md) | Provider-neutral API configuration notes |
| [references/](./references/) | Figure templates, plotting rules, prompt templates, API notes |
| [scripts/](./scripts/) | Image generation, plotting, setup checks, wizard scripts |
| [examples/figure-briefs/](./examples/figure-briefs/) | Reusable figure brief examples |
| [docs/examples/](./docs/examples/) | Showcase images, prompts, and notes |
| [templates/figure-brief/](./templates/figure-brief/) | Platform-neutral figure brief templates |
| [adapters/](./adapters/) | Claude Code and future platform adapters |

## What It Is Not

- Not a full paper-upload web platform.
- Not a replacement for checking scientific truth, labels, and numeric values.
- Not a single prompt that treats plots, diagrams, and schematics as the same task.
- Not a place to commit real API keys or private provider relay details.

## Notes

- Keep real API keys outside the repository.
- Prefer local plotting for exact quantitative figures.
- Keep provider-specific private relay details out of public docs unless clearly marked as optional examples.
- For exact publication plots, never rely on image generation for the values, axes, or benchmark geometry.

## License

MIT License. See [LICENSE](./LICENSE).
