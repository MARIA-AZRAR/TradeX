from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_alert_email(email, message):
    
    send_mail("Price Alert", 
              message,
              "noreply@gmail.com",
              [email],
              fail_silently=False)