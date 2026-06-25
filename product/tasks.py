from celery import shared_task
from time import sleep


@shared_task
def add(x, y):
    sleep(15)
    print(f"{x + y}")
    return x + y
