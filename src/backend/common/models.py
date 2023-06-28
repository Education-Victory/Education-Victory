from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Solution


class User(AbstractUser):
    avatar = models.URLField(max_length=1024, blank=True,
                             help_text="URL for avatar")
    abilityId = models.ForeignKey(
        settings.QUESTION_ABILITY_MODEL, on_delete=models.CASCADE, null=True)
