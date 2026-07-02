from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def add(x, y):
    sleep(15)
    print(f"{x + y}")
    return x + y


@shared_task
def log_product_creation(title, price):
    print(f"New product {title} with price {price} was created")


@shared_task
def products_count():
    from product.models import Product

    counted = Product.objects.count()

    print(f"Counted {counted} products")

    return f"Counted {counted} products"


@shared_task
def send_new_product_email(title, price, email):

    send_mail(
        "Hi! New product was created!",
        f"New product {title} with price {price} was created!",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "OK"
