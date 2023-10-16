from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Solution

def get_default_json():
    return '{}'

def get_default_ability():
    return [0] * 200

class User(AbstractUser):
    avatar = models.URLField(max_length=1000, blank=True,
                             help_text="URL for avatar")
    year_of_programming = models.BigIntegerField(blank=True, null=True)
    solved_prblem = models.BigIntegerField(blank=True, null=True)
    target = models.CharField(max_length=100, blank=True)
    ability = models.JSONField(default=get_default_ability)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_user')
    state = models.CharField(default='New', max_length=100)
    completeness = models.CharField(default='Start', max_length=100)
    question_id_lists = models.JSONField(default=get_default_json)
    category = models.CharField(max_length=100)
    practice_method = models.CharField(max_length=100)
    content = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.practice_method} - {self.created_at}'


class QuestionSubmission(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='submission_task')
    question_id = models.BigIntegerField(default=0)
    qtype = models.CharField(max_length=100)
    completeness = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemFrequency(models.Model):
    question_id = models.BigIntegerField(default=0)
    qtype = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    origin_link = models.URLField(max_length=1000, blank=True, help_text="URL for origin post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
