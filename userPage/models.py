from django.db import models

class userInfo(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    total_score = models.BigIntegerField(default=0)


class profile(models.Model):
    token = models.CharField(max_length=200, default=None)
    username = models.CharField(max_length=200, default=None)
    email = models.EmailField(default=None)
    password = models.CharField(max_length=200, default=None)