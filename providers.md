# Provider Compatibility / Provider 兼容说明

This project is intentionally provider-neutral, but it is not provider-agnostic in the sense of hiding all differences. Users still need to set the correct endpoint, auth mode, and model names for their own backend.

这个项目刻意保持 provider-neutral，但并不意味着会把所有 provider 差异都隐藏掉。用户仍然需要为自己的后端配置正确的 endpoint、认证方式和模型名称。

## Recommended Public Stance / 推荐的公开说明方式

- treat the official Google Gemini endpoint as the reference setup in public docs
- treat relays and custom providers as optional compatibility paths
- never hardcode a personal relay endpoint or private billing setup into shared instructions

- 在公开文档里，把官方 Google Gemini endpoint 作为参考配置
- 把 relay 和自定义 provider 作为可选兼容路径
- 不要把个人 relay 地址或私人计费配置硬编码到共享说明里

## Quick Compatibility Table / 快速兼容性表

| Provider type | Typical base URL | Typical auth mode | Third-party flag | High-res model handling |
| --- | --- | --- | --- | --- |
| Official Google Gemini | `https://generativelanguage.googleapis.com` | `google` | not needed | optional `NANOBANANA_HIGHRES_MODEL` |
| OpenAI Image API | `https://api.openai.com/v1` | `bearer` | not needed | optional `OPENAI_IMAGE_HIGHRES_MODEL` |
| Gemini-compatible relay | provider-specific | usually `bearer` | usually required | provider-specific model name |
| Custom internal endpoint | internal endpoint | provider-specific | usually required | provider-specific model name |

| Provider 类型 | 常见 base URL | 常见认证方式 | 是否需要第三方标记 | 高分模型处理 |
| --- | --- | --- | --- | --- |
| 官方 Google Gemini | `https://generativelanguage.googleapis.com` | `google` | 通常不需要 | 可选 `NANOBANANA_HIGHRES_MODEL` |
| OpenAI Image API | `https://api.openai.com/v1` | `bearer` | 通常不需要 | 可选 `OPENAI_IMAGE_HIGHRES_MODEL` |
| Gemini 兼容 relay | provider-specific | 通常为 `bearer` | 通常需要 | 使用 provider 自己的模型名 |
| 自定义内部 endpoint | internal endpoint | provider-specific | 通常需要 | 使用 provider 自己的模型名 |

## What Usually Changes Between Providers / 不同 Provider 通常会变化的部分

- `NANOBANANA_BASE_URL`
- model naming conventions
- auth mode (`google` vs `bearer`)
- whether a separate high-resolution model exists
- rate limits, quotas, and billing behavior
- how closely the provider follows the official API behavior

- `NANOBANANA_BASE_URL`
- 模型命名方式
- 认证方式（`google` 或 `bearer`）
- 是否存在单独的高分模型
- 限流、配额和计费行为
- 对官方 API 行为的兼容程度

## Official Google Reference Pattern / 官方 Google 参考配置

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
```

## Third-Party Relay Pattern / 第三方 Relay 参考配置

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

## OpenAI Image API Pattern / OpenAI Image API 参考配置

OpenAI is a first-class image backend for conceptual engineering figures and image edits. Use it when the user asks for ChatGPT/OpenAI-style image generation or when the local workflow has an OpenAI API key available.

OpenAI 可以作为概念图和参考图编辑的一等生图后端。当用户明确想用 ChatGPT/OpenAI 风格生图，或者本地已经配置 OpenAI API key 时，可以选择这个路径。

```env
ENGINEERING_FIGURE_IMAGE_PROVIDER=openai
OPENAI_API_KEY_FILE=$HOME/.codex/secrets/openai_api_key.txt
OPENAI_IMAGE_MODEL=gpt-image-1.5
OPENAI_IMAGE_HIGHRES_MODEL=gpt-image-1.5
OPENAI_IMAGE_QUALITY=auto
OPENAI_IMAGE_SIZE=auto
OPENAI_IMAGE_OUTPUT_FORMAT=png
```

Direct command example:

```powershell
python "$HOME/.codex/skills/engineering-figure-agent/scripts/generate_image.py" `
  --provider openai `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## Safety Notes / 安全说明

- only enable `NANOBANANA_ALLOW_THIRD_PARTY=1` when you intentionally trust the relay
- verify how the provider handles uploaded files, prompts, and API keys before sending sensitive material
- if high-resolution output matters, confirm the provider really exposes a distinct high-res model instead of assuming the default model is enough

- 只有在你明确信任该 relay 时，才启用 `NANOBANANA_ALLOW_THIRD_PARTY=1`
- 在发送敏感材料前，先确认 provider 如何处理上传文件、prompt 和 API key
- 如果高分输出很重要，请确认 provider 真的提供独立的高分模型，而不是默认假设普通模型就够用
