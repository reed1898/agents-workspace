# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Trading Notes is a comprehensive trading journal and discipline tracking application for individual investors. It supports multiple markets (cryptocurrency via Binance, US stocks via Interactive Brokers, A-shares, and Hong Kong stocks) with a focus on trading plan adherence and discipline analysis.

**Tech Stack**:
- Frontend: Next.js 15 (React 19) + TailwindCSS + shadcn/ui
- Backend: FastAPI (Python 3.11+) + PostgreSQL + Redis + Celery
- Key Libraries: CCXT (crypto exchanges), ib_insync (Interactive Brokers), SQLAlchemy 2.0, Zustand (state management)

## Architecture

### High-Level Structure

The project follows a monorepo structure with separated frontend and backend:

```
trading-notes/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/      # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── ui/          # shadcn/ui components
│   │   │   ├── layout/      # Layout components
│   │   │   └── features/    # Feature-specific components
│   │   ├── lib/             # Utilities and API client
│   │   ├── hooks/           # Custom React hooks
│   │   ├── store/           # Zustand stores
│   │   └── types/           # TypeScript types
│   └── public/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/v1/          # API endpoints (versioned)
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic layer
│   │   ├── tasks/           # Celery background tasks
│   │   └── utils/           # Helper functions
│   ├── alembic/             # Database migrations
│   └── tests/
└── docs/                    # Project documentation
```

### Core Domain Model

The application is built around these key entities (see `docs/architecture.md` for detailed schemas):

1. **Users & Accounts**: User authentication and multi-account management with account grouping
2. **Trades**: Historical trading records synced from exchanges or imported manually
3. **Positions**: Calculated current holdings with real-time P&L
4. **Trading Plans**: Pre-trade planning with entry reasons, stop-loss/take-profit, and risk assessment
5. **Trading Actions**: Operational logs linking actual trades to plans with emotion tracking
6. **Discipline Checks**: Automated and manual compliance verification against trading plans
7. **Market Prices**: Cached real-time price data from external sources

### Data Flow

**Trading Sync Flow**:
1. User triggers sync (manual or scheduled Celery task)
2. Backend fetches data from exchange API (CCXT/IB API)
3. Trades normalized and deduplicated (using external trade_id)
4. Positions recalculated from trade history
5. Market prices fetched and cached in Redis (TTL: 5 min)
6. Frontend displays updated data via REST API

**Discipline Check Flow**:
1. User creates trading plan before entry
2. Actual trades auto-linked to active plans by (account, symbol, time)
3. User records trading actions with emotion tags
4. On plan closure, automatic checks run (stop-loss execution, position size, timing)
5. System calculates deviation percentages and compliance scores
6. Results aggregated for discipline analytics

### Security Architecture

- **Authentication**: JWT tokens (access: 1hr, refresh: 30 days)
- **API Key Storage**: Fernet symmetric encryption with master key in environment variables
- **Password Hashing**: Bcrypt with cost factor 12
- **Rate Limiting**: Redis-backed (100 req/min per user, 5 login attempts)

## Development Commands

### Initial Setup

```bash
# Install PostgreSQL and Redis locally
# macOS: brew install postgresql@15 redis
# Ubuntu: apt-get install postgresql redis-server

# Start PostgreSQL and Redis
# macOS: brew services start postgresql@15 && brew services start redis
# Ubuntu: systemctl start postgresql redis

# Backend setup with venv
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head  # Run migrations

# Frontend setup
cd frontend
npm install
```

### Running the Application

```bash
# Backend (API server on :8000)
cd backend
source venv/bin/activate  # Activate venv first
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Celery worker (for async tasks) - in a separate terminal
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info

# Celery beat (for scheduled tasks) - in another terminal
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app beat --loglevel=info

# Frontend (dev server on :3000)
cd frontend
npm run dev
```

### Database Management

```bash
# Create a new migration
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest                           # Run all tests
pytest tests/test_trades.py     # Run specific test file
pytest -k "test_sync"           # Run tests matching pattern
pytest --cov=app                # With coverage report

# Frontend tests
cd frontend
npm test                        # Run unit tests
npm run test:e2e               # Run E2E tests (Playwright/Cypress)
```

### Code Quality

```bash
# Backend linting and formatting
cd backend
source venv/bin/activate
black app/                      # Format code
flake8 app/                    # Lint
mypy app/                      # Type checking

# Frontend linting and formatting
cd frontend
npm run lint                   # ESLint
npm run format                 # Prettier
npm run type-check            # TypeScript check
```

## Key Implementation Details

### API Integration Pattern

When adding new exchange integrations:
1. Create adapter in `backend/app/services/exchanges/` implementing common interface
2. Use CCXT for standardized crypto exchange access
3. Store encrypted credentials per account with `cryptography.fernet`
4. Implement retry logic with exponential backoff for API calls
5. Normalize data to internal trade format in service layer

### Position Calculation

Positions are derived from trades, not stored directly from exchanges:
```python
# Pseudo-code in services/position_service.py
def calculate_positions(account_id):
    trades = get_trades_sorted_by_time(account_id)
    positions = {}
    for trade in trades:
        if trade.side == 'buy':
            # Add to position, update weighted average cost
        elif trade.side == 'sell':
            # Reduce position
    # Save calculated positions to database
```

This ensures consistency even when exchange APIs are unavailable.

### Discipline Scoring Algorithm

Located in `backend/app/services/analytics_service.py`:
- Weighted scoring: stop_loss (40%), position_size (30%), emotion_control (30%)
- Compliance rate calculated per check type
- Final score: 0-100 scale
- Deviations tracked as percentage from planned values

### Caching Strategy

- **Market Prices**: Redis cache with 5-minute TTL
- **User Positions**: 1-minute TTL (frequently changing)
- **Analytics Data**: 30-minute TTL (computation-heavy)
- Cache keys use pattern: `{entity}:{id}:{field}`

## Important Conventions

### API Versioning
All API endpoints are under `/api/v1/`. When making breaking changes, create `/api/v2/` and maintain backwards compatibility.

### Database Models
- Use UUID for all primary keys
- Include `created_at` and `updated_at` timestamps
- Use JSONB for flexible/extensible fields (e.g., `extra_config`, `entry_signals`)
- Foreign keys must have `ON DELETE CASCADE` or `ON DELETE SET NULL` explicitly defined

### Error Handling
- Backend: Use HTTPException with appropriate status codes
- Return structured errors: `{"detail": "message", "code": "ERROR_CODE"}`
- Frontend: Centralized error handling in API client with toast notifications

### Git Workflow
- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Branch strategy: `main` (production), `develop` (staging), `feature/*`, `hotfix/*`

## Testing Requirements

### Backend
- Minimum 80% code coverage
- Unit tests for all service layer functions
- Integration tests for API endpoints using TestClient
- Mock external API calls (CCXT, IB API)

### Frontend
- Component tests for all UI components (React Testing Library)
- E2E tests for critical user flows: login → sync → view positions → create plan

## Environment Variables

Required environment variables (see `.env.example`):

**Backend**:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT signing key (generate with `openssl rand -hex 32`)
- `ENCRYPTION_KEY`: Fernet key for API credentials (generate with `Fernet.generate_key()`)
- `CORS_ORIGINS`: Comma-separated allowed origins

**Frontend**:
- `NEXT_PUBLIC_API_URL`: Backend API base URL (default: http://localhost:8000)

## Deployment

### Development
Local development uses venv for Python backend and npm for frontend with hot-reload enabled.

### Production
- **Frontend**: Deploy to Vercel with environment variable `NEXT_PUBLIC_API_URL`
- **Backend**:
  - Use Gunicorn + Uvicorn workers: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`
  - Run Celery worker and beat as separate services (systemd or supervisor)
  - Use managed PostgreSQL and Redis (recommended) or install locally
  - For Docker deployment, create Dockerfile wrapping the venv setup

## Reference Documentation

- **Full Requirements**: See `docs/requirements.md` for detailed feature specifications
- **Architecture Details**: See `docs/architecture.md` for complete data models and API specifications
- **Development Plan**: See `docs/development-plan.md` for phased implementation roadmap
