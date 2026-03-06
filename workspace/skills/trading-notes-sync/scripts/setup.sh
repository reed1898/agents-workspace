#!/bin/bash
# Setup virtual environment for trading-notes-sync scripts.
# Run once: bash scripts/setup.sh
# Then use: source .venv/bin/activate && python scripts/sync_binance.py

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$HOME/.openclaw/projects/trading-notes/backend"

echo "📦 Setting up trading-notes-sync environment..."
echo "   Skill dir: $SKILL_DIR"
echo "   Backend: $BACKEND_DIR"

cd "$SKILL_DIR"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv .venv
fi

echo "📥 Installing dependencies..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r "$BACKEND_DIR/requirements.txt"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  cd $SKILL_DIR"
echo "  source .venv/bin/activate"
echo "  python scripts/show_positions.py"
echo ""
echo "Or run directly:"
echo "  $SKILL_DIR/.venv/bin/python scripts/show_positions.py"
