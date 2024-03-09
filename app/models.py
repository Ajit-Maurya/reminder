from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField()
    time = models.TimeField() 
    sent = models.BooleanField(default=False)