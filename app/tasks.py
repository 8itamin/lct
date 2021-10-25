# Create your tasks here

from celery import shared_task

@shared_task
def print_celery():
    print('celery')


