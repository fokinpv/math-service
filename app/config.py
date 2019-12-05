import os

MAX_WORKERS = int(os.getenv('APP_MAX_WORKERS', '2'))
WORKER_TASK_TIMEOUT = float(os.getenv('APP_WORKER_TASK_TIMEOUT', '1'))
