from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Solution

class User(AbstractUser):
    avatar = models.URLField(max_length=1024, blank=True, help_text="URL for avatar")


class UserSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submission_user')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='submission_solution')
    content = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

