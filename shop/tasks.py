from celery import shared_task
from django.contrib.auth import get_user_model, settings
from django.core.mail import message, send_mail
from django.core import serializers
import json
import ast
@shared_task(bind=True)
def send_mails(self,users):
    print('hi')
    res = json.loads(users)
    for user in res:
        mail_subject="Message"
        message="Welcome:You are now part of our community"
        to_email=user["fields"]["email"]
        send_mail(subject=mail_subject,
                message=message,
                recipient_list=[to_email],
                fail_silently=True,
                from_email=settings.EMAIL_HOST_USER
                )
    return "done"

@shared_task(bind=True)
def send_mails1(self,users):
    print('hi')
    res = json.loads(users)
    for user in res:
        mail_subject="Message"
        message="thanks your item has been created"
        to_email=user["fields"]["email"]
        send_mail(subject=mail_subject,
                message=message,
                recipient_list=[to_email],
                fail_silently=True,
                from_email=settings.EMAIL_HOST_USER
                )
    return "done"

@shared_task(bind=True)
def send_mails2(self,users):
    print('hi')
    res = json.loads(users)
    for user in res:
        mail_subject="Message"
        message="thanks your item has been deleted"
        to_email=user["fields"]["email"]
        send_mail(subject=mail_subject,
                message=message,
                recipient_list=[to_email],
                fail_silently=True,
                from_email=settings.EMAIL_HOST_USER
                )
    return "done"

@shared_task(bind=True)
def send_mails3(self,users):
    print('hi')
    res = json.loads(users)
    for user in res:
        mail_subject="Message"
        message="New order has been registered"
        to_email=user["fields"]["email"]
        send_mail(subject=mail_subject,
                message=message,
                recipient_list=[to_email],
                fail_silently=True,
                from_email=settings.EMAIL_HOST_USER
                )
    return "done"

