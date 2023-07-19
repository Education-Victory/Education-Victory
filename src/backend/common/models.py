from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Solution


class User(AbstractUser):
    name = models.CharField(max_length=100)
    avatar = models.URLField(
        max_length=1024, blank=True, help_text="URL for avatar")
    info = models.JSONField(help_text='data: [1, 2, 0]')
    ability = models.JSONField(help_text='data: [10, 20, 10]')


class UserSubmission(models.Model):
    user_id = models.BigIntegerField(
        help_text='user_id (settings.AUTH_USER_MODEL.id)')
    question_id = models.BigIntegerField(help_text='question id (Question.id)')
    solution_id = models.BigIntegerField(help_text='solution_id (Solution.id)')
    hash_code = models.CharField(max_length=200)
    code = models.JSONField(blank=True, help_text='code in submission')
    completeness = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
