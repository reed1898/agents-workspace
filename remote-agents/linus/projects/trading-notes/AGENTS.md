# Repository Guidelines

## Project Structure & Module Organization
- `backend/` hosts the FastAPI app. Core code lives in `backend/app/` with `api/` (v1 routes), `models/` (SQLAlchemy), `schemas/` (Pydantic), `services/`, and `tasks/` (Celery). Database migrations are in `backend/alembic/`.
- `frontend/` is a Next.js App Router app. Pages are in `frontend/app/`, shared UI in `frontend/components/`, and API clients/types in `frontend/lib/` and `frontend/types/`.
- `docs/` and `PROGRESS.md` capture architecture, requirements, and roadmap notes. `data/` contains sample CSV inputs.

## Build, Test, and Development Commands
- Backend bootstrap: `./start-backend.sh` (installs deps, runs Alembic, starts Uvicorn on :8000).
- Backend dev server: `cd backend && uvicorn app.main:app --reload`.
- Backend migrations: `cd backend && alembic upgrade head`.
- Backend tests: `cd backend && pytest`.
- Frontend dev server: `./start-frontend.sh` or `cd frontend && npm run dev` (runs on :3000).
- Frontend build/lint: `cd frontend && npm run build` and `npm run lint`.

## Coding Style & Naming Conventions
- Python: follow Black formatting and Flake8 linting (`black app/`, `flake8 app/`). Keep modules snake_case and classes PascalCase.
- TypeScript/React: follow ESLint defaults (`npm run lint`). Use PascalCase for components and camelCase for hooks/utilities.
- Use descriptive filenames (e.g., `trade_import_service.py`, `KlineChart.tsx`).

## Testing Guidelines
- Backend uses `pytest`; name tests `test_*.py` and colocate near feature scripts or in a dedicated tests folder if added later.
- No frontend test runner is configured yet; add one (e.g., Playwright) if you introduce complex UI logic.

## Commit & Pull Request Guidelines
- Git history mixes plain summaries and Conventional Commit prefixes (e.g., `feat:`, `docs:`). Prefer short, imperative subjects and include a prefix when it clarifies scope.
- PRs should include: a concise summary, testing steps (`pytest`, `npm run lint`, etc.), and UI screenshots when changing frontend views.

## Configuration & Secrets
- Backend expects `backend/.env` (see `backend/.env.example`) and a running Postgres/Redis.
- Frontend expects `frontend/.env.local` with `NEXT_PUBLIC_API_URL` and OAuth client IDs.
