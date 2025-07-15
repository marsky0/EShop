from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "shop_tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

import app.tasks.email as email

__all__ = ["email"]
