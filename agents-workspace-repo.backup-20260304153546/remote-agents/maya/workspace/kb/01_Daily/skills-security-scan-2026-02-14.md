# Skills Security Scan — 2026-02-14 (UTC)

Nightly static audit (non-destructive).

## Tonight summary (<=10 lines)
- Scanned roots:
  - /home/ubuntu/.openclaw/workspace/skills
  - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills
  - /home/ubuntu/.openclaw/skills
- Skill directories found: 93
- Risk distribution: high=1, medium=7, low=85
- ⚠️ High risk skills detected: yes (review the high-risk entries below)
- Total risky-pattern grep hits (global): 231
- Report file: /home/ubuntu/.openclaw/kb/01_Daily/skills-security-scan-2026-02-14.md

## Detailed findings (by skill)

- Skill: 1password
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password/SKILL.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password/references/get-started.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/1password/references/cli-examples.md\n

- Skill: apple-notes
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-notes
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-notes/SKILL.md\n

- Skill: apple-reminders
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-reminders
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/apple-reminders/SKILL.md\n

- Skill: bear-notes
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bear-notes/SKILL.md\n

- Skill: blogwatcher
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blogwatcher/SKILL.md\n

- Skill: blucli
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blucli
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/blucli/SKILL.md\n

- Skill: bluebubbles
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bluebubbles
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=1; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bluebubbles/SKILL.md:18:- Attachment `path` for local files, or `buffer` + `filename` for base64
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bluebubbles/SKILL.md\n

- Skill: camsnap
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/camsnap
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/camsnap/SKILL.md\n

- Skill: canvas
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=2; net=1; eval=1; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:55:| `eval`     | Execute JavaScript in the canvas     |
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:161:3. Test URL directly: `curl http://<hostname>:18793/__openclaw__/canvas/<file>.html`
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md\n

- Skill: clawhub
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/clawhub
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/clawhub/SKILL.md\n

- Skill: coding-agent
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/coding-agent
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md\n

- Skill: discord
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/discord/SKILL.md\n

- Skill: eightctl
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/eightctl
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/eightctl/SKILL.md\n

- Skill: food-order
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/food-order
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/food-order/SKILL.md\n

- Skill: gemini
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gemini
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gemini/SKILL.md\n

- Skill: gifgrep
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gifgrep
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gifgrep/SKILL.md\n

- Skill: github
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/github
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/github/SKILL.md\n

- Skill: gog
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gog
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/gog/SKILL.md\n

- Skill: goplaces
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/goplaces
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/goplaces/SKILL.md\n

- Skill: healthcheck
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/healthcheck
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/healthcheck/SKILL.md\n

- Skill: himalaya
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/SKILL.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/references/message-composition.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/himalaya/references/configuration.md\n

- Skill: imsg
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/imsg
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/imsg/SKILL.md\n

- Skill: local-places
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=8; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:35:1. **Check server:** `curl http://127.0.0.1:8000/ping`
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:40:curl -X POST http://127.0.0.1:8000/locations/resolve \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:48:curl -X POST http://127.0.0.1:8000/places/search \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:61:curl http://127.0.0.1:8000/places/{place_id}
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:56:Example search request (curl):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:59:curl -X POST http://127.0.0.1:8000/places/search \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:78:Example resolve request (curl):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:81:curl -X POST http://127.0.0.1:8000/locations/resolve \
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/pyproject.toml
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/schemas.py
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/src/local_places/main.py\n

- Skill: mcporter
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/mcporter/SKILL.md\n

- Skill: model-usage
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage/scripts/model_usage.py
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage/SKILL.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/model-usage/references/codexbar-cli.md\n

- Skill: nano-banana-pro
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=4; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py:149:                # inline_data.data is already bytes, not base64
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py:152:                    # If it's a string, it might be base64
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py:153:                    import base64
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py:154:                    image_data = base64.b64decode(image_data)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/SKILL.md\n

- Skill: nano-pdf
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-pdf
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/nano-pdf/SKILL.md\n

- Skill: notion
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=9; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:35:curl -X GET "https://api.notion.com/v1/..." \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:48:curl -X POST "https://api.notion.com/v1/search" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:58:curl "https://api.notion.com/v1/pages/{page_id}" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:66:curl "https://api.notion.com/v1/blocks/{page_id}/children" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:74:curl -X POST "https://api.notion.com/v1/pages" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:90:curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:103:curl -X POST "https://api.notion.com/v1/data_sources" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:121:curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md:131:curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/notion/SKILL.md\n

- Skill: obsidian
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/obsidian
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/obsidian/SKILL.md\n

- Skill: openai-image-gen
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=6; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:10:        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:3:import base64
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:176:    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:178:        print("Missing OPENAI_API_KEY", file=sys.stderr)
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:224:            filepath.write_bytes(base64.b64decode(image_b64))
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md\n

- Skill: openai-whisper
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper/SKILL.md\n

- Skill: openai-whisper-api
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=8; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:10:        "requires": { "bins": ["curl"], "env": ["OPENAI_API_KEY"] },
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:16:# OpenAI Whisper API (curl)
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:42:Set `OPENAI_API_KEY`, or configure it in `~/.openclaw/openclaw.json`:
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:59:if [[ "${OPENAI_API_KEY:-}" == "" ]]; then
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:60:  echo "Missing OPENAI_API_KEY" >&2
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:75:curl -sS https://api.openai.com/v1/audio/transcriptions \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:76:  -H "Authorization: Bearer $OPENAI_API_KEY" \
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md\n

- Skill: openhue
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openhue
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openhue/SKILL.md\n

- Skill: oracle
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=1; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle/SKILL.md:86:- Auto-pick: `api` when `OPENAI_API_KEY` is set; otherwise `browser`.
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/oracle/SKILL.md\n

- Skill: ordercli
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/ordercli/SKILL.md\n

- Skill: peekaboo
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/peekaboo
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/peekaboo/SKILL.md\n

- Skill: sag
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sag
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sag/SKILL.md\n

- Skill: session-logs
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/session-logs
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/session-logs/SKILL.md\n

- Skill: sherpa-onnx-tts
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=8; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:5:const { spawnSync } = require("node:child_process");
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:19:  const value = explicit || process.env.SHERPA_ONNX_RUNTIME_DIR || "";
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:24:  const value = explicit || process.env.SHERPA_ONNX_MODEL_DIR || "";
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:29:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_MODEL_FILE || "").trim();
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:44:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_TOKENS_FILE || "").trim();
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:51:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_DATA_DIR || "").trim();
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:144:const env = { ...process.env };
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:157:const child = spawnSync(
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/SKILL.md
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts\n

- Skill: skill-creator
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/__pycache__/quick_validate.cpython-312.pyc
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/license.txt
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py\n

- Skill: slack
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/slack
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/slack/SKILL.md\n

- Skill: songsee
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/songsee
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/songsee/SKILL.md\n

- Skill: sonoscli
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sonoscli
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sonoscli/SKILL.md\n

- Skill: spotify-player
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/spotify-player
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/spotify-player/SKILL.md\n

- Skill: summarize
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=1; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:60:- OpenAI: `OPENAI_API_KEY`
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md\n

- Skill: things-mac
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/things-mac/SKILL.md\n

- Skill: tmux
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/wait-for-text.sh
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/scripts/find-sessions.sh
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/tmux/SKILL.md\n

- Skill: trello
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=11; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:28:All commands use curl to hit the Trello REST API.
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:33:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:39:curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:45:curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:51:curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:60:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:67:curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:74:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:88:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:91:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:94:curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md\n

- Skill: video-frames
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames/scripts/frame.sh
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/video-frames/SKILL.md\n

- Skill: voice-call
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/voice-call
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/voice-call/SKILL.md\n

- Skill: wacli
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/wacli
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/wacli/SKILL.md\n

- Skill: weather
  - Path: /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=6; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:5:metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:17:curl -s "wttr.in/London?format=3"
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:24:curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:31:curl -s "wttr.in/London?T"
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:42:- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`
    - /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:49:curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md\n

- Skill: clawra-selfie
  - Path: /home/ubuntu/.openclaw/skills/clawra-selfie
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=12; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:4:allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:240:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/skills/clawra-selfie/SKILL.md:283:    credentials: process.env.FAL_KEY!
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
    - /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh:137:    curl -s -X POST "$GATEWAY_URL/message" \
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.ts
    /home/ubuntu/.openclaw/skills/clawra-selfie/scripts/clawra-selfie.sh
    /home/ubuntu/.openclaw/skills/clawra-selfie/assets/clawra.png\n

- Skill: find-skills
  - Path: /home/ubuntu/.openclaw/skills/find-skills
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.openclaw/skills/find-skills/_meta.json
    /home/ubuntu/.openclaw/skills/find-skills/.clawhub/origin.json
    /home/ubuntu/.openclaw/skills/find-skills/SKILL.md\n

- Skill: knowledge-base-collector
  - Path: /home/ubuntu/.openclaw/skills/knowledge-base-collector
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/tagger.py
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/weekly_digest.py
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/wechat_backlog.py
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_url.py
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/search_kb.py
    - /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/ingest_image.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    mtime: most recently modified files (top 3)
    /home/ubuntu/.openclaw/skills/knowledge-base-collector/SKILL.md
    /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/__pycache__/weekly_digest.cpython-312.pyc
    /home/ubuntu/.openclaw/skills/knowledge-base-collector/scripts/__pycache__/wechat_backlog.cpython-312.pyc\n

- Skill: Gmail
  - Path: /home/ubuntu/.openclaw/workspace/skills/Gmail
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=7; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    - /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:245:- Message body is base64url encoded in the `raw` field
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: YouTube
  - Path: /home/ubuntu/.openclaw/workspace/skills/YouTube
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: Gmail.disabled-20260208-062106
  - Path: /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=7; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:245:- Message body is base64url encoded in the `raw` field
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: claw-roam.disabled-20260208-081734
  - Path: /home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/_disabled/claw-roam.disabled-20260208-081734/scripts/claw-roam.sh
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: a-stock-analysis
  - Path: /home/ubuntu/.openclaw/workspace/skills/a-stock-analysis
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/portfolio.py
    - /home/ubuntu/.openclaw/workspace/skills/a-stock-analysis/scripts/analyze.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: avatarkit
  - Path: /home/ubuntu/.openclaw/workspace/skills/avatarkit
  - SKILL.md: yes
  - package.json: yes
  - Risk: low
    - Reason: hits=3; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/example.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/image.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/SKILL.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/avatar.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/memory.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/natural.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/voice.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/index.ts
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:154:      formData.append('audio', Buffer.from(options.audioData, 'base64'), {
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts:22:  referenceImage?: string; // URL or base64
    - /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts:67:  audioData: Buffer | string; // Buffer or base64
  - Changes:
    git: clean

- Skill: backend
  - Path: /home/ubuntu/.openclaw/workspace/skills/avatarkit/backend
  - SKILL.md: no
  - package.json: yes
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: clean

- Skill: browse
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=21; net=1; eval=1; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:45:stagehand eval "document.querySelector('.price').textContent"
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:155:Invoke with curl:
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:157:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:188:curl -X POST https://api.browserbase.com/v1/functions/<function-id>/invoke \
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:253:  const data = await page.$$eval(selector, els =>
    - /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:376:- [ ] Verify with curl
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:68:stagehand eval "document.querySelector('.new-class')?.textContent"
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:161:| `stagehand eval <js>` | Run diagnostic JS |
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:187:> stagehand eval "document.querySelector('.product-price')?.textContent"
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:128:Then invoke locally via curl:
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/auth/SKILL.md:193:stagehand eval "document.querySelector('input[type=password]')?.id"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: auth
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse/skills/auth
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=1; net=0; eval=1; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/auth/SKILL.md:193:stagehand eval "document.querySelector('input[type=password]')?.id"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: browser-automation
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse/skills/browser-automation
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: create
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse/skills/create
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=2; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:128:Then invoke locally via curl:
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: fix
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=3; net=0; eval=1; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:68:stagehand eval "document.querySelector('.new-class')?.textContent"
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:161:| `stagehand eval <js>` | Run diagnostic JS |
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:187:> stagehand eval "document.querySelector('.product-price')?.textContent"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: functions
  - Path: /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=9; net=1; eval=1; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:34:eval "$(stagehand fn auth export)"
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:147:### Via curl
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:174:        'x-bb-api-key': process.env.BROWSERBASE_API_KEY!,
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:187:      { headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY! } }
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:209:  const items = await page.$$eval(params.selector, els => 
    - /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:275:eval "$(stagehand fn auth export)"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: claw-roam
  - Path: /home/ubuntu/.openclaw/workspace/skills/claw-roam
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/claw-roam/scripts/claw-roam.sh
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: clawra
  - Path: /home/ubuntu/.openclaw/workspace/skills/clawra
  - SKILL.md: yes
  - package.json: yes
  - Risk: low
    - Reason: hits=27; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js
    - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts
    - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:12:const { execSync, spawn } = require("child_process");
    - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:88:    execSync(`which ${cmd}`, { stdio: "ignore" });
    - /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:109:    execSync(cmd, { stdio: "ignore" });
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:4:allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:240:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:283:    credentials: process.env.FAL_KEY!
    - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
    - /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: skill
  - Path: /home/ubuntu/.openclaw/workspace/skills/clawra/skill
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=12; net=1; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:4:allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:240:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:283:    credentials: process.env.FAL_KEY!
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
    - /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: crypto-price
  - Path: /home/ubuntu/.openclaw/workspace/skills/crypto-price
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/crypto-price/scripts/get_price_chart.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: crypto-watch
  - Path: /home/ubuntu/.openclaw/workspace/skills/crypto-watch
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/crypto-watch/scripts/crypto_watch.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: db-readonly
  - Path: /home/ubuntu/.openclaw/workspace/skills/db-readonly
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/db-readonly/scripts/db_readonly.sh
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: deepwiki
  - Path: /home/ubuntu/.openclaw/workspace/skills/deepwiki
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/deepwiki/scripts/deepwiki.js
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: deepwork-tracker
  - Path: /home/ubuntu/.openclaw/workspace/skills/deepwork-tracker
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: find-skills
  - Path: /home/ubuntu/.openclaw/workspace/skills/find-skills
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: github
  - Path: /home/ubuntu/.openclaw/workspace/skills/github
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: gmail-auto-processor
  - Path: /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor
  - SKILL.md: yes
  - package.json: yes
  - Risk: low
    - Reason: hits=34; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/generate-report.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.sh
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/task-monitor.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:1:const { execSync } = require('child_process');
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:9:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread category:promotions" maxResults=100', { encoding: 'utf8' });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:21:    execSync(`mcporter call --server google-workspace --tool "gmail.modify" messageId="${msgId}" removeLabelIds='["INBOX","UNREAD"]'`, { encoding: 'utf8', timeout: 10000 });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:32:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1', { encoding: 'utf8' });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:7:const { execSync } = require('child_process');
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:45:    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:8:const { execSync } = require('child_process');
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:47:    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:58:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:69:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:8:const { execSync } = require('child_process');
    - /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:17:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: google-workspace-mcp
  - Path: /home/ubuntu/.openclaw/workspace/skills/google-workspace-mcp
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: imap-smtp-email
  - Path: /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email
  - SKILL.md: yes
  - package.json: yes
  - Risk: low
    - Reason: hits=16; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/setup.sh
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:38:    host: process.env.SMTP_HOST,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:39:    port: parseInt(process.env.SMTP_PORT) || 587,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:40:    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:42:      user: process.env.SMTP_USER,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:43:      pass: process.env.SMTP_PASS,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:46:      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:70:    from: options.from || process.env.SMTP_FROM || process.env.SMTP_USER,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:125:      from: process.env.SMTP_FROM || process.env.SMTP_USER,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:126:      to: process.env.SMTP_USER, // Send to self
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:23:const DEFAULT_MAILBOX = process.env.IMAP_MAILBOX || 'INBOX';
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:50:    user: process.env.IMAP_USER,
    - /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:51:    password: process.env.IMAP_PASS,
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: larksuite-wiki
  - Path: /home/ubuntu/.openclaw/workspace/skills/larksuite-wiki
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/larksuite-wiki/larksuite-wiki.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: obsidian-integration
  - Path: /home/ubuntu/.openclaw/workspace/skills/obsidian-integration
  - SKILL.md: yes
  - package.json: yes
  - Risk: low
    - Reason: hits=1; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js:3:const { execSync } = require('child_process');
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: reminder
  - Path: /home/ubuntu/.openclaw/workspace/skills/reminder
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/reminder/scripts/reminder-scheduler.sh
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: self-reflection
  - Path: /home/ubuntu/.openclaw/workspace/skills/self-reflection
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: skill-vetter
  - Path: /home/ubuntu/.openclaw/workspace/skills/skill-vetter
  - SKILL.md: yes
  - package.json: no
  - Risk: high
    - Reason: hits=8; net=1; eval=1; sudo=1; ssh=1; binaries=0
  - Scripts (sample):
    - (none found in first 30)
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:38:• curl/wget to unknown URLs
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:41:• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:43:• Uses base64 decode on anything
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:44:• Uses eval() or exec() with external input
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:49:• Requests elevated/sudo permissions
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:112:curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:115:curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'
    - /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:118:curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: stock_analysis
  - Path: /home/ubuntu/.openclaw/workspace/skills/stock_analysis
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=7; net=1; eval=0; sudo=1; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/analyze_stock.sh
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/stock_analyzer.py
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:13:sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:16:无 sudo 降级：
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:46:If your system lacks `python3-pip` or you don't have sudo access, the script will suggest fallback options:
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:49:# User-level installation without sudo
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:23:  echo "sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git"
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:35:echo "\n无法 sudo 时的降级路径（推荐）："
    - /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:36:echo "1) curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py"
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: task-status
  - Path: /home/ubuntu/.openclaw/workspace/skills/task-status
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/monitor_task.py
    - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/test_send_status.py
    - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_websocket.py
    - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status_with_logging.py
    - /home/ubuntu/.openclaw/workspace/skills/task-status/scripts/send_status.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: technews
  - Path: /home/ubuntu/.openclaw/workspace/skills/technews
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/article_fetcher.py
    - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/techmeme_scraper.py
    - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/social_reactions.py
    - /home/ubuntu/.openclaw/workspace/skills/technews/scripts/technews.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: trading-journal
  - Path: /home/ubuntu/.openclaw/workspace/skills/trading-journal
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/trading-journal/scripts/trade-log.sh
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: ui-ux-pro-max
  - Path: /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max
  - SKILL.md: yes
  - package.json: no
  - Risk: medium
    - Reason: hits=8; net=0; eval=0; sudo=1; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/design_system.py
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/core.py
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/__init__.py
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/scripts/search.py
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-README.md:304:sudo apt update && sudo apt install python3
    - /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-skill-content.md:22:sudo apt update && sudo apt install python3
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: vercel-cli
  - Path: /home/ubuntu/.openclaw/workspace/skills/vercel-cli
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=6; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js
  - Risky pattern matches (sample):
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:7:const { execSync } = require('child_process');
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:17:    const result = execSync(`vercel ${args}`, {
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:30:    execSync('which vercel', { stdio: 'pipe' });
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:43:      execSync('npm install -g vercel', { stdio: 'inherit' });
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:56:        execSync('vercel login', { stdio: 'inherit' });
    - /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:90:        execSync('vercel logs', { stdio: 'inherit', cwd: projectPath });
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json

- Skill: webapp-testing
  - Path: /home/ubuntu/.openclaw/workspace/skills/webapp-testing
  - SKILL.md: yes
  - package.json: no
  - Risk: low
    - Reason: hits=0; net=0; eval=0; sudo=0; ssh=0; binaries=0
  - Scripts (sample):
    - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/element_discovery.py
    - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/console_logging.py
    - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/examples/static_html_automation.py
    - /home/ubuntu/.openclaw/workspace/skills/webapp-testing/scripts/with_server.py
  - Risky pattern matches (sample):
    - (no matches)
  - Changes:
    git: dirty (up to 50 lines)
     M .clawhub/lock.json
     M .transcribed-audio.txt
     M HEARTBEAT.md
     M IDENTITY.md
     M MEMORY.md
     M SOUL.md
     D knowledge/README.md
     D knowledge/_Templates/Daily.md
     D knowledge/_Templates/Project-Review.md
     D knowledge/_Templates/Trading-Review.md
     M memory/us_intraday_risk_cursor.json
     M reminders/events.yml
     M skills/find-skills/.clawhub/origin.json
     M skills/stock_analysis/SKILL.md
    ?? .agents/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh
    ?? .clawhub/lock.sync-conflict-20260208-163217-3MIRDQS.json
    ?? .task-monitor.md
    ?? .venv/
    ?? avatarkit-api-private/
    ?? avatarkit-api/
    ?? crypto-watch/market-snapshot.json
    ?? gmail-archive-promotions.js
    ?? kb
    ?? memory/2026-02-08.md
    ?? memory/2026-02-11.md
    ?? memory/ashare_intraday_risk_cursor.json
    ?? memory/avatarkit-project.md
    ?? memory/cron-jobs.md
    ?? memory/syncthing-test-2026-02-08.md
    ?? memory/us_intraday_watch_state.json
    ?? mission-control/
    ?? node_modules/
    ?? reports/a-stock-report-2026-02-13.md
    ?? share/
    ?? skills/Gmail/
    ?? skills/avatarkit/
    ?? skills/claw-roam/
    ?? skills/gmail-auto-processor/
    ?? skills/obsidian-integration/
    ?? skills/reminder/.clawhub/
    ?? skills/reminder/SKILL.sync-conflict-20260208-083216-R4LZGWG.md
    ?? skills/reminder/_meta.json
    ?? skills/reminder/scripts/
    ?? skills/stock_analysis/outputs/
    ?? skills/vercel-cli/
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.json
    ?? tmp/a_preopen_2026-02-12/000547.SZ_20260212T005048Z.txt
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.json
    ?? tmp/a_preopen_2026-02-12/000592.SZ_20260212T005049Z.txt
    ?? tmp/a_preopen_2026-02-12/002291.SZ_20260212T005051Z.json


## Global grep hits (raw excerpt, top 200 lines)

- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:1:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:9:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread category:promotions" maxResults=100', { encoding: 'utf8' });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:21:    execSync(`mcporter call --server google-workspace --tool "gmail.modify" messageId="${msgId}" removeLabelIds='["INBOX","UNREAD"]'`, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/archive-promotions.js:32:    const result = execSync('mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1', { encoding: 'utf8' });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:7:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-processor.js:45:    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:8:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:47:    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:58:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-anxiety-free.js:69:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:8:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:17:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/smart-run.js:28:    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:8:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:43:    const result = execSync(cmd, { encoding: 'utf8', timeout: timeoutMs });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:55:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index-fixed.js:66:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:10:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:64:    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:74:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:84:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/index.js:95:    execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/task-monitor.js:3:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:8:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:16:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:27:    const result = execSync(cmd, { encoding: 'utf8', timeout: 120000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/batch-process.js:84:    execSync('sleep 2');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js:6:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/gmail-quick.js:32:    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:7:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:20:    const result = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/test-archive.js:31:    execSync(cmd, { encoding: 'utf8', timeout: 15000 });
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js:8:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/gmail-auto-processor/subagent-run.js:16:    const result = execSync(cmd, { encoding: 'utf8', timeout: 10000 });
- /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:12:const { execSync, spawn } = require("child_process");
- /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:88:    execSync(`which ${cmd}`, { stdio: "ignore" });
- /home/ubuntu/.openclaw/workspace/skills/clawra/bin/cli.js:109:    execSync(cmd, { stdio: "ignore" });
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:4:allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:240:import { exec } from "child_process";
- /home/ubuntu/.openclaw/workspace/skills/clawra/SKILL.md:283:    credentials: process.env.FAL_KEY!
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:4:allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:107:curl -X POST "https://fal.run/xai/grok-imagine-image/edit" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:142:curl -X POST "http://localhost:18789/message" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:209:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:240:import { exec } from "child_process";
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/SKILL.md:283:    credentials: process.env.FAL_KEY!
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:16:import { exec } from "child_process";
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:99:  const falKey = process.env.FAL_KEY;
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:162:    process.env.OPENCLAW_GATEWAY_URL || "http://localhost:18789";
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.ts:163:  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:82:RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image" \
- /home/ubuntu/.openclaw/workspace/skills/clawra/skill/scripts/clawra-selfie.sh:136:    curl -s -X POST "$GATEWAY_URL/message" \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
- /home/ubuntu/.openclaw/workspace/skills/_disabled/Gmail.disabled-20260208-062106/SKILL.md:245:- Message body is base64url encoded in the `raw` field
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:7:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:17:    const result = execSync(`vercel ${args}`, {
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:30:    execSync('which vercel', { stdio: 'pipe' });
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:43:      execSync('npm install -g vercel', { stdio: 'inherit' });
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:56:        execSync('vercel login', { stdio: 'inherit' });
- /home/ubuntu/.openclaw/workspace/skills/vercel-cli/vercel-skill.js:90:        execSync('vercel logs', { stdio: 'inherit', cwd: projectPath });
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:19:curl -s -X GET 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10' \
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:58:curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE' \
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:65:curl -s -X POST 'https://ctrl.maton.ai/connections' \
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:74:curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:95:curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:223:      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
- /home/ubuntu/.openclaw/workspace/skills/Gmail/SKILL.md:245:- Message body is base64url encoded in the `raw` field
- /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/api.ts:154:      formData.append('audio', Buffer.from(options.audioData, 'base64'), {
- /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts:22:  referenceImage?: string; // URL or base64
- /home/ubuntu/.openclaw/workspace/skills/avatarkit/src/types.ts:67:  audioData: Buffer | string; // Buffer or base64
- /home/ubuntu/.openclaw/workspace/skills/obsidian-integration/index.js:3:const { execSync } = require('child_process');
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:45:stagehand eval "document.querySelector('.price').textContent"
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:155:Invoke with curl:
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:157:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:188:curl -X POST https://api.browserbase.com/v1/functions/<function-id>/invoke \
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:253:  const data = await page.$$eval(selector, els =>
- /home/ubuntu/.openclaw/workspace/skills/browse/SKILL.md:376:- [ ] Verify with curl
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:68:stagehand eval "document.querySelector('.new-class')?.textContent"
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:161:| `stagehand eval <js>` | Run diagnostic JS |
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/fix/SKILL.md:187:> stagehand eval "document.querySelector('.product-price')?.textContent"
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:128:Then invoke locally via curl:
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/create/SKILL.md:130:curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/auth/SKILL.md:193:stagehand eval "document.querySelector('input[type=password]')?.id"
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:34:eval "$(stagehand fn auth export)"
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:119:curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:147:### Via curl
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:151:curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:159:curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:174:        'x-bb-api-key': process.env.BROWSERBASE_API_KEY!,
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:187:      { headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY! } }
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:209:  const items = await page.$$eval(params.selector, els => 
- /home/ubuntu/.openclaw/workspace/skills/browse/skills/functions/SKILL.md:275:eval "$(stagehand fn auth export)"
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:38:• curl/wget to unknown URLs
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:41:• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:43:• Uses base64 decode on anything
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:44:• Uses eval() or exec() with external input
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:49:• Requests elevated/sudo permissions
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:112:curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:115:curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'
- /home/ubuntu/.openclaw/workspace/skills/skill-vetter/SKILL.md:118:curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:13:sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/PRE_RELEASE_CHECKLIST.md:16:无 sudo 降级：
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:46:If your system lacks `python3-pip` or you don't have sudo access, the script will suggest fallback options:
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/SKILL.md:49:# User-level installation without sudo
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:23:  echo "sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git"
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:35:echo "\n无法 sudo 时的降级路径（推荐）："
- /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/install_deps.sh:36:echo "1) curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py"
- /home/ubuntu/.openclaw/workspace/skills/ai-video-generation/SKILL.md:24:curl -fsSL https://cli.inference.sh | sh && infsh login
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/assets/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nextjs.csv:37:36,Environment,Validate env vars,Check required env vars exist,Validate on startup,Undefined env at runtime,if (!process.env.DATABASE_URL) throw,process.env.DATABASE_URL (might be undefined),High,
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:53:52,Environment,Use runtimeConfig for env vars,Access environment variables safely,runtimeConfig in nuxt.config,process.env directly,"runtimeConfig: { apiSecret: '', public: { apiBase: '' } }",process.env.API_SECRET in components,High,https://nuxt.com/docs/guide/going-further/runtime-config
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/data/stacks/nuxtjs.csv:55:54,Environment,Access public config with useRuntimeConfig,Get public config in components,useRuntimeConfig().public,Direct process.env access,const config = useRuntimeConfig(); config.public.apiBase,process.env.NUXT_PUBLIC_API_BASE,High,https://nuxt.com/docs/api/composables/use-runtime-config
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-README.md:304:sudo apt update && sudo apt install python3
- /home/ubuntu/.openclaw/workspace/skills/ui-ux-pro-max/references/upstream-skill-content.md:22:sudo apt update && sudo apt install python3
- /home/ubuntu/.openclaw/workspace/skills/x-search/SKILL.md:106:- The script uses curl to query the xAI Responses API endpoint
- /home/ubuntu/.openclaw/workspace/skills/x-search/scripts/x_search.sync-conflict-20260208-163216-3MIRDQS.sh:87:RESPONSE=$(curl -s "${API_HOST}/v1/responses" \
- /home/ubuntu/.openclaw/workspace/skills/x-search/scripts/x_search.sh:93:RESPONSE=$(curl -s "${API_HOST}/v1/responses" \
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:38:    host: process.env.SMTP_HOST,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:39:    port: parseInt(process.env.SMTP_PORT) || 587,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:40:    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:42:      user: process.env.SMTP_USER,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:43:      pass: process.env.SMTP_PASS,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:46:      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:70:    from: options.from || process.env.SMTP_FROM || process.env.SMTP_USER,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:125:      from: process.env.SMTP_FROM || process.env.SMTP_USER,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js:126:      to: process.env.SMTP_USER, // Send to self
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:23:const DEFAULT_MAILBOX = process.env.IMAP_MAILBOX || 'INBOX';
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:50:    user: process.env.IMAP_USER,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:51:    password: process.env.IMAP_PASS,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:52:    host: process.env.IMAP_HOST || '127.0.0.1',
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:53:    port: parseInt(process.env.IMAP_PORT) || 1143,
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:54:    tls: process.env.IMAP_TLS === 'true',
- /home/ubuntu/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js:56:      rejectUnauthorized: process.env.IMAP_REJECT_UNAUTHORIZED !== 'false',
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:10:        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:3:import base64
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:176:    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:178:        print("Missing OPENAI_API_KEY", file=sys.stderr)
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py:224:            filepath.write_bytes(base64.b64decode(image_b64))
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/bluebubbles/SKILL.md:18:- Attachment `path` for local files, or `buffer` + `filename` for base64
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:28:All commands use curl to hit the Trello REST API.
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:33:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:39:curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:45:curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:51:curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:60:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:67:curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:74:curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:88:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:91:curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/trello/SKILL.md:94:curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:10:        "requires": { "bins": ["curl"], "env": ["OPENAI_API_KEY"] },
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:11:        "primaryEnv": "OPENAI_API_KEY",
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:16:# OpenAI Whisper API (curl)
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/SKILL.md:42:Set `OPENAI_API_KEY`, or configure it in `~/.openclaw/openclaw.json`:
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:59:if [[ "${OPENAI_API_KEY:-}" == "" ]]; then
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:60:  echo "Missing OPENAI_API_KEY" >&2
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:75:curl -sS https://api.openai.com/v1/audio/transcriptions \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh:76:  -H "Authorization: Bearer $OPENAI_API_KEY" \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md:60:- OpenAI: `OPENAI_API_KEY`
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:55:| `eval`     | Execute JavaScript in the canvas     |
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/canvas/SKILL.md:161:3. Test URL directly: `curl http://<hostname>:18793/__openclaw__/canvas/<file>.html`
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:5:metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:17:curl -s "wttr.in/London?format=3"
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:24:curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:31:curl -s "wttr.in/London?T"
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:42:- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md:49:curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:5:const { spawnSync } = require("node:child_process");
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:19:  const value = explicit || process.env.SHERPA_ONNX_RUNTIME_DIR || "";
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:24:  const value = explicit || process.env.SHERPA_ONNX_MODEL_DIR || "";
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:29:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_MODEL_FILE || "").trim();
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:44:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_TOKENS_FILE || "").trim();
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:51:  const explicit = (explicitFlag || process.env.SHERPA_ONNX_DATA_DIR || "").trim();
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:144:const env = { ...process.env };
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/sherpa-onnx-tts/bin/sherpa-onnx-tts:157:const child = spawnSync(
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:35:1. **Check server:** `curl http://127.0.0.1:8000/ping`
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:40:curl -X POST http://127.0.0.1:8000/locations/resolve \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:48:curl -X POST http://127.0.0.1:8000/places/search \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SKILL.md:61:curl http://127.0.0.1:8000/places/{place_id}
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:56:Example search request (curl):
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:59:curl -X POST http://127.0.0.1:8000/places/search \
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:78:Example resolve request (curl):
- /home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/local-places/SERVER_README.md:81:curl -X POST http://127.0.0.1:8000/locations/resolve \

