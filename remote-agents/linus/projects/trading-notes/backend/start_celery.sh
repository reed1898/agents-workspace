#!/bin/bash
# Celery Worker 启动脚本

cd "$(dirname "$0")"
source venv/bin/activate
celery -A app.core.celery_app:celery_app worker --loglevel=info
