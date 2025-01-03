from celery import Celery

app = Celery(
    "myapi",
    broker="redis://redis_manager:6379/0",
    backend="redis://redis_manager:6379/0",
)
