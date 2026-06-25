from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(code, email):

    send_mail(
        "Привет новый пользователь!",
        f"Вот подавись! Твой код: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "OK"


@shared_task
def delete_unactive_users():
    from users.models import CustomUser

    deleted = CustomUser.objects.filter(is_active=False).delete()
    return f"DELETED {deleted}"
