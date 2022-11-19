from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Message(models.Model):
    text = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    sender = models.ForeignKey('users.User', related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey('users.User', related_name='receiver', on_delete=models.CASCADE)
    file = models.FileField(upload_to='audio/', blank=True, null=True)
