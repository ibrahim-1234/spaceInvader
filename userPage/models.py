from django.db import models

class userInfo(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    total_score = models.BigIntegerField(default=0)   
