# Platform Adapters

Adapters keep platform-specific instructions outside the core Codex skill.

| Adapter | Status | Purpose |
|---|---|---|
| `claude-code/` | Initial usable adapter | Install as a Claude Code skill for local figure-brief, prompt, and plot workflows. |

The core contracts remain platform-neutral:

- `../docs/figure-brief-spec.md`
- `../schemas/figure-brief.schema.json`
- `../schemas/plot-request.schema.json`
- `../docs/prompt-pack.md`
