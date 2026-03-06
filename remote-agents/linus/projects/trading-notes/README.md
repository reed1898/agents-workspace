# Trading Notes

Trading Notes is a trading journal and discipline tracking application for
individual investors. The repo is a monorepo with a FastAPI backend and a
Next.js frontend.

## Features

- FastAPI backend with JWT auth scaffolding, Alembic migrations, and core
  services wiring.
- Next.js frontend with TailwindCSS and shadcn/ui foundations.
- MySQL and Redis integrations (plus Celery for background tasks).
- Documentation for setup, quick start, and architecture.

## Project layout

```
backend/   # FastAPI application
frontend/  # Next.js application
docs/      # Requirements, architecture, and plans
```

## Getting started

Full instructions live in `SETUP.md` and `QUICKSTART.md`. The short version:

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Configuration

- `backend/.env` contains database, Redis, security keys, and OAuth settings.
  See `backend/.env.example` for defaults.
- `frontend/.env.local` should define `NEXT_PUBLIC_API_URL` and OAuth client
  settings (see `QUICKSTART.md`).

## Docs

- `SETUP.md` for environment setup
- `QUICKSTART.md` for the current onboarding steps
- `PROGRESS.md` for status tracking
- `docs/architecture.md` for system design
