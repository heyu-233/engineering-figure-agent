# Provider Selection

Use this reference when configuring or choosing an image backend.

## Public Stance

- Treat the official Google Gemini endpoint as the public reference setup.
- Treat relays and custom providers as optional compatibility paths.
- Never hardcode personal relay endpoints or private billing details into shared docs.
- OpenAI Image API is a first-class backend for conceptual figures and edits.

## Provider Matrix

| Provider | Base URL | Auth | Third-party flag | High-res handling |
|---|---|---|---|---|
| Official Google Gemini | `https://generativelanguage.googleapis.com` | `google` | not needed | optional `NANOBANANA_HIGHRES_MODEL` |
| OpenAI Image API | `https://api.openai.com/v1` | bearer | not needed | optional `OPENAI_IMAGE_HIGHRES_MODEL` |
| Gemini-compatible relay | provider-specific | usually bearer | usually required | provider-specific |
| OpenAI-compatible relay | provider-specific | usually bearer | usually required | provider-specific |

## Gemini / Banana Environment

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
NANOBANANA_API_KEY_FILE=$HOME/.codex/secrets/nanobanana_api_key.txt
```

For a trusted relay:

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

## OpenAI Environment

```env
ENGINEERING_FIGURE_IMAGE_PROVIDER=openai
OPENAI_API_KEY_FILE=$HOME/.codex/secrets/openai_api_key.txt
OPENAI_IMAGE_MODEL=gpt-image-1.5
OPENAI_IMAGE_HIGHRES_MODEL=<optional-final-quality-model>
OPENAI_IMAGE_QUALITY=auto
OPENAI_IMAGE_SIZE=auto
OPENAI_IMAGE_OUTPUT_FORMAT=png
```

## Safety Rules

- Only set `NANOBANANA_ALLOW_THIRD_PARTY=1` when the user intentionally trusts the provider.
- Only set `OPENAI_ALLOW_THIRD_PARTY=1` when the user intentionally trusts a non-official OpenAI-compatible endpoint.
- Verify how uploaded prompts, images, and API keys are handled before sending sensitive material.
- If the user asks for ChatGPT/OpenAI-style generation, use `--provider openai` and `OPENAI_*` settings. Do not route OpenAI requests through Gemini relay settings.
