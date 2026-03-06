# Trading Notes Backend

FastAPI backend for Trading Notes application.

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Generate secret keys:
```bash
# SECRET_KEY
openssl rand -hex 32

# ENCRYPTION_KEY (for API keys)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

5. Update `.env` with your configuration

## Database Setup

1. Create MySQL database:
```bash
mysql -u root -p -e "CREATE DATABASE trading_notes DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;"
```

2. Run migrations:
```bash
alembic upgrade head
```

## Running

Start the development server:
```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000
API docs at: http://localhost:8000/api/v1/docs

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black app/
```

Lint:
```bash
flake8 app/
```
