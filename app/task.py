# import celery
from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reminder
from celery import shared_task

@shared_task
def send_remainder_email(remainder_id):
    try:
        reminder = Reminder.objects.get(id=remainder_id)
    except Reminder.DoesNotExist:
        return
    
    current_datetime = timezone.now()
    reminder_datetime = timezone.make_aware(timezone.datetime.combine(reminder.date, reminder.time))
    time_until_reminder = reminder_datetime - current_datetime

    if time_until_reminder.total_seconds() > 0:
        send_remainder_email.apply_async((remainder_id,), countdown=time_until_reminder.total_seconds())
    else:
        subject = 'Reminder: {}'.format(reminder.message)
        message = 'This is a reminder for: {}'.format(reminder.message)
        send_mail(subject, message, 'django@mail.com', ['mauryaajit.am@gmail.com'],fail_silently=False,)