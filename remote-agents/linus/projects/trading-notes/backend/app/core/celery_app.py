"""
Celery 应用配置
"""
from celery import Celery
from .config import settings

# 创建 Celery 应用
celery_app = Celery(
    "trading_notes",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.sync_tasks"]
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 分钟超时
    task_soft_time_limit=25 * 60,  # 25 分钟软超时
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)
