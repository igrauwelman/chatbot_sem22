from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bot(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    classpath = models.CharField(max_length=512, null=False)
    avatar = models.CharField(max_length=1024, null=True)
    active = models.BooleanField(default=True)


class ChatSession(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user_message = models.BooleanField()
    content = models.CharField(max_length=8192)
    mkdate = models.DateTimeField(auto_now_add=True)




