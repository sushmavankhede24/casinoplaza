from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    wallet_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.username