"""
Common setup for all trading-notes-sync scripts.

Handles:
- Loading .env from workspace
- Adding trading-notes backend to sys.path
- Patching pydantic Settings so the project code can import without its own .env
- Creating standalone SQLAlchemy sessions
- Fetching accounts from database
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List

# ── 1. Load workspace .env ──────────────────────────────────────────────────

WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
DOTENV_PATH = WORKSPACE_DIR / ".env"

def _load_dotenv_simple(path: Path) -> None:
    """Minimal .env loader (no dependency on python-dotenv)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        os.environ.setdefault(key, value)

_load_dotenv_simple(DOTENV_PATH)

# ── 2. Resolve key env vars ─────────────────────────────────────────────────

DATABASE_URL = os.environ.get("TRADING_NOTES_DATABASE_URL")
ENCRYPTION_KEY = os.environ.get("TRADING_NOTES_ENCRYPTION_KEY")
SECRET_KEY = os.environ.get("TRADING_NOTES_SECRET_KEY")

if not DATABASE_URL:
    print("❌ TRADING_NOTES_DATABASE_URL not set. Add to ~/.zshrc")
    sys.exit(1)

if not ENCRYPTION_KEY:
    print("❌ TRADING_NOTES_ENCRYPTION_KEY not set. Add to ~/.zshrc")
    sys.exit(1)

# ── 3. Add trading-notes backend to sys.path ────────────────────────────────

PROJECT_BACKEND = Path.home() / ".openclaw" / "projects" / "trading-notes" / "backend"
if not PROJECT_BACKEND.exists():
    print(f"❌ trading-notes backend not found at {PROJECT_BACKEND}")
    sys.exit(1)

if str(PROJECT_BACKEND) not in sys.path:
    sys.path.insert(0, str(PROJECT_BACKEND))

# ── 4. Patch project Settings before any project import ─────────────────────
#
# The project uses pydantic-settings `Settings()` which reads its own .env.
# We patch the env vars it expects so instantiation succeeds even without
# the project's .env file present.

os.environ.setdefault("DATABASE_URL", DATABASE_URL)
os.environ.setdefault("ENCRYPTION_KEY", ENCRYPTION_KEY)
os.environ.setdefault("SECRET_KEY", SECRET_KEY or "cli-placeholder-secret")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

# ── 5. Now safe to import project modules ────────────────────────────────────

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.trade_account import TradeAccount

# Create our own engine (separate from the project's)
_engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
_SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db() -> Session:
    """Create a new database session."""
    return _SessionFactory()


def get_accounts(
    db: Session,
    account_name: Optional[str] = None,
    account_type: Optional[str] = None,
    broker: Optional[str] = None,
    active_only: bool = True,
) -> List[TradeAccount]:
    """Query trade accounts with optional filters."""
    query = db.query(TradeAccount)
    if active_only:
        query = query.filter(TradeAccount.is_active == True)
    if account_name:
        query = query.filter(TradeAccount.account_name == account_name)
    if account_type:
        query = query.filter(TradeAccount.account_type == account_type)
    if broker:
        query = query.filter(TradeAccount.broker == broker)
    return query.all()


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging and return the root logger."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    # Silence noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logging.getLogger("trading-sync")
