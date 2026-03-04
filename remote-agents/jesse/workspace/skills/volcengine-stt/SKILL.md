---
name: volcengine-stt
description: Transcribe audio to text using Volcano Engine (Volcengine/ARK) speech-to-text APIs. Use when the user wants to replace Whisper/OpenAI STT with Volcengine, transcribe Telegram/Discord voice notes via Volcengine, or build a reusable STT skill for other OpenClaw agents.
---

# Volcengine STT

Use this skill to run speech-to-text through Volcengine.

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg
```

Default behavior:
- Mode: `standard` (submit + query)
- Endpoint: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit` + `/query`
- Resource ID: `${VOLC_RESOURCE_ID:-volc.seedasr.auc}`
- Output file: `<input>.txt`

## Required env

- `VOLC_APP_ID` (X-Api-App-Key)
- `VOLC_ACCESS_TOKEN` (X-Api-Access-Key)

Optional:
- `VOLC_RESOURCE_ID` (default: `volc.seedasr.auc`)
- `VOLC_STT_MODE` (`standard` or `flash`, default `standard`)

## Useful flags

```bash
# Save plain text to custom path
{baseDir}/scripts/transcribe.sh ./voice.ogg --out /tmp/voice.txt

# Return raw JSON (for debugging/integration)
{baseDir}/scripts/transcribe.sh ./voice.ogg --json --out /tmp/voice.json

# Hint language
{baseDir}/scripts/transcribe.sh ./voice.ogg --language zh-CN

# Use flash API explicitly (requires flash entitlement)
{baseDir}/scripts/transcribe.sh ./voice.ogg --mode flash --resource-id volc.bigasr.auc_turbo
```

## Integration notes

- For OpenClaw voice-message handling, call this script instead of Whisper script.
- Keep keys in machine-local config or env, never commit secrets.
- If your account lacks flash entitlement, stay on default `standard` mode with `volc.seedasr.auc`.
