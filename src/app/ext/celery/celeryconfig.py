import os

# Using broker
broker_url = os.environ.get('CELERY_BROKER_URL')

# Using the database to store tasks state and results.
result_backend = os.environ.get('CELERY_RESULT_BACKEND')

# Ignore task result by default
task_ignore_result = os.environ.get('CELERY_TASK_IGNORE_RESULT')
