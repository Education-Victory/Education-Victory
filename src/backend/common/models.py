from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Solution


class User(AbstractUser):
    avatar = models.URLField(max_length=1024, blank=True,
                             help_text="URL for avatar")
    ability_id = models.ForeignKey(
        settings.QUESTION_ABILITY_MODEL, on_delete=models.CASCADE, null=True)


class UserSubmission(models.Model):
    # Representation of the user_id (settings.AUTH_USER_MODEL.id)
    user_id = models.BigIntegerField()
    # Representation of the question id (Question.id)
    question_id = models.BigIntegerField()
    # List of category ids, should be validated
    category_id_list = models.JSONField()
    # Representation of the solution_id (Solution.id)
    solution_id = models.BigIntegerField()
    keypoint = models.JSONField(
        blank=True, help_text='list of completed keypoint id')
    # User submission details
    #   Should contain a 'score' key that represent the score of this submission, integer, [0,100]
    details = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
