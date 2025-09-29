from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_activation_email(subject, message, from_email, recipient_list):
    send_mail(
        subject, 
        message,
        from_email, 
        recipient_list, 
        )

@shared_task
def send_password_reset_email(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
    )