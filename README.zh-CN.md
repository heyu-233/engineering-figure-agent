# Engineering Figure Agent

<div align="center">

![Codex Skill](https://img.shields.io/badge/Codex-skill-111827)
![Claude Code](https://img.shields.io/badge/Claude%20Code-adapter-8b5cf6)
![Modes](https://img.shields.io/badge/modes-image%20%7C%20plot-f59e0b)
![Backends](https://img.shields.io/badge/backends-Gemini%20%7C%20OpenAI%20%7C%20local%20plots-16a34a)

**面向工程与计算机论文的 agent-native 配图工具。**

概念图走 `image mode`，精确定量图走 `plot mode`，不要把所有论文图都当成同一种生图 prompt。

[GitHub 首页](./README.md) | [English Guide](./README.en.md) | [示例图库](./docs/examples/README.md) | [Showcase](./docs/showcase.md)

</div>

## 快速预览

| 系统架构图 | 协同感知图 | 安全分类图 |
|---|---|---|
| ![Federated open-vocabulary driving figure](docs/examples/federated-open-vocab-driving-2k-1.png) | ![Cooperative object tracking figure](docs/examples/cooperative-object-tracking-2k-1.png) | ![Multi-agent safety overview figure](docs/examples/multi-agent-safety-overview-2k-1.png) |

| Dense Overview | 本地精确绘图 |
|---|---|
| ![Linux kernel system diagram](docs/examples/linux-kernel-system-1.jpg) | ![Benchmark plot](docs/examples/benchmark-plot.png) |

## 适合什么

| 需求 | 推荐路径 |
|---|---|
| 系统架构图、算法流程图、graphical abstract、硬件框图 | `image mode` |
| benchmark、ablation、trend、heatmap、scatter、多面板实验图 | `plot mode` |
| 一张图里既有概念图又有实验图 | 先本地渲染定量 panel，再处理概念 panel |
| 只想规划图怎么画 | 先写 `figure brief` |

## 快速开始

安装和检查：

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
```

只生成 prompt，不调用网络：

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/efa.py" prompt `
  --figure-template system-architecture `
  --lang zh `
  "一个包含 OCR、切分、嵌入、向量检索、重排序和答案生成的 RAG 系统。"
```

渲染精确图表：

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/efa.py" plot `
  "$HOME/.codex/skills/engineering-figure-agent/docs/examples/benchmark-plot-request.json" `
  --out-path output/benchmark-plot
```

## 标准工作流

1. 先写或整理 `figure brief`：图的目标、论文主张、图类型、面板、必须保留标签、数据和验收清单。
2. 判断模式：概念表达用 `image mode`，精确数值用 `plot mode`。
3. 对概念图生成 prompt，对定量图生成 plot request。
4. 生成输出后检查：标签、箭头、层级、数值、坐标轴、图例和论文主张是否一致。

## 平台适配

| 平台 | 入口 | 用途 |
|---|---|---|
| Codex | `SKILL.md` | 主体验，适合本地脚本和 agent workflow |
| Claude Code | `adapters/claude-code/` | 本地项目里的 figure brief、prompt、plot 工作流 |
| ChatGPT / Claude 网页 | `docs/prompt-pack.md` | 复制 prompt 使用 |
| VS Code / Obsidian | `templates/figure-brief/` | 管理 figure brief、prompt、plot request |

核心规范：

- `docs/figure-brief-spec.md`
- `schemas/figure-brief.schema.json`
- `schemas/plot-request.schema.json`

## Provider

| 后端 | 用途 |
|---|---|
| Gemini / Banana-compatible | 概念图生成、参考图编辑 |
| OpenAI Image API | ChatGPT/OpenAI 风格概念图生成与编辑 |
| Local plot | 精确数值图表 |

真实 API key 不要提交到仓库。第三方 relay 必须显式设置 `NANOBANANA_ALLOW_THIRD_PARTY=1`。

## 项目边界

- 它不是完整 Web 平台。
- 它不替代论文主张判断和审稿式图评估。
- 它不会为你编造实验数值、硬件参数或性能提升。
- 对于精确图表，不要使用图像模型绘制数值、坐标轴或 benchmark 几何关系。

## 目录

| 路径 | 说明 |
|---|---|
| `SKILL.md` | Codex skill 核心规则 |
| `scripts/` | prompt 构建、生图、绘图、检查和统一 CLI |
| `references/` | 模板、provider、高分策略、中文标签和绘图规则 |
| `docs/examples/` | 示例图、prompt、figure brief |
| `templates/figure-brief/` | 平台无关 figure brief 模板 |
| `adapters/` | Claude Code 等平台适配 |

## License

MIT License. See [LICENSE](./LICENSE).
