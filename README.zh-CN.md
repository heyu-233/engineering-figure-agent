# Engineering Figure Agent

`engineering-figure-agent` 不是一个通用配图平台，而是一个面向 agent 工作流的工程论文配图 skill，专门把概念图和精确定量图分开处理。

## 项目定位

这个仓库主要服务于工程与计算机论文中的图形生产层，而不是一个完整的论文上传平台。

它更适合：

- 已经知道自己需要什么图的研究者
- 希望把论文配图接入 Codex / agent 工作流的人
- 需要同时处理方法图和定量图的人
- 计算机、系统、算法、电子、嵌入式方向的作者

它不主打：

- 完整 Web 平台
- 上传论文后一键包办所有环节
- 面向所有学科的通用学术插图

## 核心差异化

### 1. 面向 agent，而不是面向平台表单

- 更适合接在研究写作、代码、实验分析工作流之后
- 可以作为 Codex skill 直接调用
- 更强调可控性、可组合性和可复用性

### 2. 概念图和定量图分开处理

- `image mode`：适合系统架构图、算法流程图、graphical abstract、工程示意图
- `plot mode`：适合柱状图、趋势图、热力图、散点图、多面板 publication plot

这点很关键：它不把所有论文图都当作同一种通用生图任务来处理。

### 3. 更偏工程 / CS 论文，而不是泛学科

- system architecture
- algorithm workflow
- hardware block diagram
- benchmark / ablation / heatmap / scatter

### 4. 更强调准确性与可读性

- 白底、清晰层级、短标签
- 中英技术标签混合可读
- 定量图优先本地精确绘制
- 适合导出 `png / pdf / svg`

## 推荐工作流

最推荐的用法是两步走：

1. 先用 `ai-research-writing-guide` 确定：
   - 图要支持什么 claim
   - 图的类型
   - 面板结构 / 模块结构
   - caption 要保留什么信息
2. 再用 `engineering-figure-agent` 生成最终图

建议上游传给本 skill 的字段：

- figure goal
- figure type
- panel plan / module list
- must-keep terms
- output language
- visual constraints

## 可选上游 skill：ai-research-writing-guide

`ai-research-writing-guide` 是推荐的上游 skill，但不是强制依赖。

它主要负责：

- 先从论文内容里梳理 figure goal
- 帮你判断该用什么图
- 产出 panel plan / module plan
- 保留 caption logic 和 must-keep terms

`engineering-figure-agent` 本身可以单独使用。  
如果你已经知道自己要画什么图，可以直接使用本 skill，不需要先安装上游 skill。

如果你想走更完整的工作流：

`论文内容 -> figure brief -> 最终出图`

那就建议额外安装 `ai-research-writing-guide`。

推荐安装位置：

- `$HOME/.codex/skills/ai-research-writing-guide`

例如：

```powershell
git clone https://github.com/Leey21/awesome-ai-research-writing $HOME/.codex/skills/ai-research-writing-guide
```

安装后建议：

1. 重启 Codex
2. 在对话里显式提到 `ai-research-writing-guide`
3. 先做一次 figure brief 或段落分析测试

例如：

- `用 ai-research-writing-guide 帮我从这段方法部分整理一个 figure brief`

如果 Codex 能按这个上游写作/规划 workflow 响应，说明识别正常。

### 第三方上游说明

- `ai-research-writing-guide` 是推荐配合使用的上游 skill
- 其写作侧内容来源参考第三方仓库 [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)
- 本项目仅说明推荐的工作流集成方式，不声明对该第三方仓库的所有权，也不保证其结构、可用性或未来版本始终保持不变
- 如果你选择直接安装该第三方仓库，请先确认其当前结构仍然适合作为 Codex skill 使用

## 仓库结构

- `README.md`：GitHub 首页双语 landing
- `README.zh-CN.md`：中文完整说明
- `README.en.md`：英文完整说明
- `SKILL.md`：Codex skill 内部说明
- `scripts/`：安装、检查、prompt 构建、图片生成、定量绘图
- `references/`：模板与论文风格参考
- `examples/figure-briefs/`：可直接复用的 figure brief 模板
- `docs/examples/`：公开示例图和说明
- `providers.md`：provider 兼容说明

## 两种模式

### `image mode`

适合：

- 系统架构图
- 算法流程图
- 图形摘要
- 电子 / 嵌入式示意图
- 参考风格重绘

当结构表达比数值精确更重要时，用这个模式。

`image mode` 现在可以选择两类后端：

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --provider openai `
  --model gpt-image-1.5 `
  --figure-template system-architecture `
  --lang zh `
  "一个包含 OCR、切分、嵌入、向量检索、重排序和答案生成的 RAG 系统。"
```

OpenAI 路径使用 `OPENAI_API_KEY` 或 `OPENAI_API_KEY_FILE`；原来的 Google Gemini / Banana 兼容路径继续使用 `NANOBANANA_*` 配置。

### `plot mode`

适合：

- benchmark 柱状图
- ablation 图
- trend curve
- heatmap
- scatter
- 多面板结果图

当数值、坐标、几何关系必须保持准确时，用这个模式。

经验法则：

- 如果数值真实性重要，用 `plot mode`
- 如果图是概念表达，用 `image mode`
- 如果一张图里两者都有，先本地渲染定量部分，再补概念部分

## Platform Support

目前主要验证平台仍然是 Windows，但 `engineering-figure-agent` 的核心工作流并不局限于 Windows。

- 已经有用户在 macOS 上成功安装并使用
- 有些场景下也可以通过 AI 辅助完成安装，而不一定需要全程手动配置
- 核心 Python 工作流通常可以运行在 Windows / macOS / Linux 上
- 需要注意的是，部分辅助脚本目前仍然更偏向 Windows / PowerShell

仓库里最容易跨平台使用的部分是：

- `scripts/build_engineering_figure_prompt.py`
- `scripts/build_plot_spec.py`
- `scripts/plot_publication_figure.py`
- `scripts/generate_image.py`

如果你使用的是 macOS 或 Linux，下面的小节更适合作为 fallback 指南和环境参考，而不是唯一安装方式。

## Windows 最短安装路径

如果你第一次安装，只想走一条最短路径，可以直接在 PowerShell 里按顺序执行：

```powershell
git clone https://github.com/heyu-233/engineering-figure-agent $HOME/.codex/skills/engineering-figure-agent
Copy-Item $HOME/.codex/skills/engineering-figure-agent/secrets/nanobanana.env.example $HOME/.codex/secrets/nanobanana.env
Copy-Item $HOME/.codex/skills/engineering-figure-agent/secrets/nanobanana_api_key.txt.example $HOME/.codex/secrets/nanobanana_api_key.txt
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

然后：

1. 编辑 `nanobanana.env` 和 `nanobanana_api_key.txt`
2. 重启 Codex
3. 再开始实际生成图片

## 第一次安装后要重启 Codex

这一步很重要，建议明确做一次。

原因很简单：

- 新安装的 skill 需要让 Codex 重新扫描 skill 目录
- 新增的环境变量、脚本和本地配置也更适合在新会话里生效

推荐做法：

1. 完成安装和 secrets 配置
2. 关闭当前 Codex 会话
3. 重新打开 Codex
4. 再测试 skill 是否被识别

## macOS / Linux Setup Notes

虽然仓库里的部分辅助脚本主要面向 Windows，但核心工作流在 macOS 和 Linux 上是可以使用的，而且已经有成功安装案例。

很多情况下，正常安装流程或 AI 辅助安装就已经足够。  
如果你的环境仍然需要手动调整，可以参考下面这组 fallback 步骤：

```bash
git clone https://github.com/heyu-233/engineering-figure-agent ~/.codex/skills/engineering-figure-agent
mkdir -p ~/.codex/secrets
cp ~/.codex/skills/engineering-figure-agent/secrets/nanobanana.env.example ~/.codex/secrets/nanobanana.env
cp ~/.codex/skills/engineering-figure-agent/secrets/nanobanana_api_key.txt.example ~/.codex/secrets/nanobanana_api_key.txt
python3 -m pip install -r ~/.codex/skills/engineering-figure-agent/requirements.txt
```

然后：

1. 编辑 `~/.codex/secrets/nanobanana.env`
2. 把 `~/.codex/secrets/nanobanana_api_key.txt` 里的占位符换成真实 key
3. 重启 Codex
4. 跑一个最小 Python 脚本测试

例如：

```bash
python3 ~/.codex/skills/engineering-figure-agent/scripts/generate_image.py \
  --figure-template system-architecture \
  --print-prompt \
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

如果你不想依赖加载脚本，也可以在自己的 shell 会话里手动 `export` 环境变量，或者从自己的 shell 配置文件中加载。

常见需要额外手动调整的原因包括：

- shell 差异
- Python 环境差异
- 本地代理配置
- provider 侧 API 或认证方式差异

## 快速开始

### 1. 放到 Codex skill 目录

```powershell
$HOME/.codex/skills/engineering-figure-agent
```

### 2. 配置本地 secrets

在仓库外准备：

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

模板见：

- `secrets/nanobanana.env.example`
- `secrets/nanobanana_api_key.txt.example`

### 3. 跑安装与检查

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/install_and_test.ps1" -RunSetupCheck
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

### 4. 加载环境变量

```powershell
. "$HOME/.codex/skills/engineering-figure-agent/scripts/load_nanobanana_env.ps1"
```

### 5. 跑一个最小示例

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## 最小可用 provider 配置模板

### 方案 1：官方 Gemini

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

### 方案 2：第三方 Gemini 兼容 relay

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
NANOBANANA_API_KEY_FILE=C:/Users/sly92/.codex/secrets/nanobanana_api_key.txt
```

建议：

- 只有在你明确接受第三方 relay 时才设置 `NANOBANANA_ALLOW_THIRD_PARTY=1`
- 如果你只想先验证链路，先用默认模型跑一张图，不要一上来就走 high-res

## 安装后如何验证 skill 已被 Codex 识别

可以用这几种方式确认：

### 方法 1：在对话里直接点名 skill

例如：

- `用 engineering-figure-agent 帮我生成一个系统架构图 prompt`
- `用 engineering-figure-agent 帮我画一个 benchmark 柱状图`

如果 Codex 能按这个 skill 的规则响应，说明识别正常。

### 方法 2：先跑 setup 脚本

```powershell
& "$HOME/.codex/skills/engineering-figure-agent/scripts/check_setup.ps1"
```

这个脚本能帮助你快速确认：

- skill 路径是否正确
- secrets 是否存在
- 依赖是否齐全

### 方法 3：测试最小 prompt 生成链

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --figure-template system-architecture `
  --print-prompt `
  "A retrieval system with OCR, embedding, vector search, reranking, and answer synthesis."
```

如果能打印出完整 prompt，说明本地脚本链已经工作正常。

## 常见失败与解决办法

### `python` not found

- 确认 PowerShell 能执行 `python --version`
- 如果不行，先安装 Python 并勾选加入 PATH

### API key 文件还是 placeholder

- 打开 `$HOME/.codex/secrets/nanobanana_api_key.txt`
- 把示例占位符替换成真实 key
- 确保只有一行，没有多余说明文字

### 第三方 relay 被安全检查拦截

- 如果你使用 relay，需要在 env 里加：
  - `NANOBANANA_ALLOW_THIRD_PARTY=1`
- 否则生成脚本会拒绝发送请求

### high-res 请求直接中止

- 检查是否配置了 `NANOBANANA_HIGHRES_MODEL`
- 检查 provider 是否真的支持高分模型
- 如果 high-res 失败，不要期待脚本自动 silent fallback

### `load_nanobanana_env.ps1` 报 secrets 不存在

- 确认以下文件存在：
  - `$HOME/.codex/secrets/nanobanana.env`
  - `$HOME/.codex/secrets/nanobanana_api_key.txt`

### 定量图脚本报依赖缺失

- 执行：

```powershell
pip install -r "$HOME/.codex/skills/engineering-figure-agent/requirements.txt"
```

## 示例图

当前仓库包含：

- 自动驾驶高密度总览图
- 协同目标跟踪图
- 多智能体安全总览图
- Linux kernel 系统架构图
- 一张补充性的健康监测与预警系统部署场景参考图

说明见：

- `docs/examples/README.md`

## 为什么值得中英双语

这个仓库长期保持中英双语是有价值的：

- GitHub 自然传播更偏英文
- 小红书 / CSDN / 小黑盒传播更偏中文
- 目标用户既包括国内研究生，也包括国际 agent / open-source 用户
- 双语能明显降低理解门槛

推荐文档策略：

- `README.md`：双语 landing
- `README.zh-CN.md`：中文完整说明
- `README.en.md`：英文完整说明
- 后续重要文档如 `providers.md` 也可以逐步双语化

## 项目简介

`engineering-figure-agent` 是一个面向工程与计算机论文的 agent-native figure skill：概念图走图像模型，定量图走本地精确渲染。它更强调图形生产流程的可控性、学术风格约束和定量结果的准确表达，而不是把所有论文图都当作同一种通用生图任务来处理。

## 注意事项

- 不要把真实 API Key 提交到仓库
- 定量图尽量使用本地绘图链
- 公共文档里尽量不要硬编码私人 relay 地址
