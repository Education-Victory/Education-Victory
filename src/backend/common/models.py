from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.URLField(max_length=1024, blank=True, help_text="URL for avatar")
