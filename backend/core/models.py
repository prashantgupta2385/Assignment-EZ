from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('OPS', 'Operations'),
        ('CLIENT', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)  # for email verification
