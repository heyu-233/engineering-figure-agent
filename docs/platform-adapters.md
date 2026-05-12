# Platform Adapters

Engineering Figure Agent is Codex-first, but the figure brief, prompt pack, and plot request formats are platform-neutral.

## Adapter Matrix

| Platform | Best use | Entry |
|---|---|---|
| Codex | Full skill workflow with local scripts and validation | Root `SKILL.md` |
| Claude Code | Local repository figure work and prompt/plot generation | `adapters/claude-code/` |
| Claude / ChatGPT web | Prompt-only figure planning and refinement | `docs/prompt-pack.md` |
| VS Code | Editing briefs, JSON specs, and rendered outputs | `templates/`, `schemas/`, `scripts/` |
| Obsidian | Keeping figure briefs and prompt history as notes | Markdown templates |
| Future CLI | One command for prompt, image, plot, check, and wizard | `scripts/efa.py` |

## Claude Code

Install the Claude Code adapter as a project skill or user skill, then ask:

```text
Use the engineering-figure-agent skill. Create a figure brief, choose image or plot mode, and generate the prompt or plot files for this engineering paper figure.
```

Chinese:

```text
使用 engineering-figure-agent skill。先整理 figure brief，再判断 image mode / plot mode，最后生成工程论文配图 prompt 或精确定量图。
```

## Chat-Only Assistants

Use `docs/prompt-pack.md`. Paste the paper context, figure goal, table values, and any must-keep labels. Ask the assistant to return a figure brief before producing a final prompt.

## VS Code / Obsidian

Store:

```text
figure-brief.md
plot-request.json
prompt.txt
output/
```

Keep generated prompts and output paths near the figure brief so the figure can be revised later.

## Adapter Rules

- Preserve the image/plot mode boundary.
- Keep exact numeric plots local and deterministic.
- Do not hide provider-specific differences.
- Keep real API keys outside the repository.
- Treat generated diagrams as drafts until labels, layout, and scientific claims are checked.
