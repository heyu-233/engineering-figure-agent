# High-Resolution Policy

Use this reference when the user asks for 2K, high-resolution, final-export, or final-quality output.

## Rules

- Use the normal default model for routine generation.
- Use `NANOBANANA_HIGHRES_MODEL` only when the request clearly indicates high resolution or final export.
- Use `OPENAI_IMAGE_HIGHRES_MODEL` only when a distinct OpenAI high-resolution or final-quality model is configured.
- A one-off `--model` override is allowed when the user explicitly names a provider model.

## Fail-Closed Behavior

If high-resolution output is requested and the high-resolution path is unavailable or fails:

- Stop immediately.
- Do not silently downgrade to a cheaper or lower-tier model.
- Ask the human whether to retry high-resolution generation or explicitly allow fallback.

This applies to missing model settings, HTTP 429, upstream errors, and network failures.

## Hint Words

Treat these as high-resolution intent:

- `2k`
- `highres`
- `high-res`
- `high resolution`
- `final export`
- `final quality`
