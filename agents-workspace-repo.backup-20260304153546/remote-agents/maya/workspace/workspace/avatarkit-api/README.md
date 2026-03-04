# AvatarKit API (Internal)

Internal avatar generation API for OpenClaw skill.

## Quick Start

```bash
# Set API keys (required for generation)
export FAL_KEY="your_fal_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"

# Run with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000/docs

## Endpoints

- `POST /api/v1/avatars` - Create avatar
- `GET /api/v1/avatars` - List avatars
- `GET /api/v1/avatars/{id}` - Get avatar
- `PUT /api/v1/avatars/{id}` - Update avatar
- `DELETE /api/v1/avatars/{id}` - Delete avatar
- `POST /api/v1/avatars/{id}/reference` - Upload reference image

- `POST /api/v1/generate/image` - Generate image
- `POST /api/v1/generate/voice` - Generate voice

## Storage

- Files saved to `./storage/` locally (default)
- Or set R2_* env vars to use Cloudflare R2
