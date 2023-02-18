from django.db import models
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=30, help_text='category of solution')
    weight = models.IntegerField(default=1, help_text='weight of the category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    class QuestionTypeChoice(models.TextChoices):
        OTHERS = 'OT', 'Others'
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        SHORT_ANSWER = 'SA', 'Short Answer'
        TRUE_O_FALSE = 'TF', 'True / False'

    name = models.CharField(max_length=100, blank=True, help_text='question name')
    description = models.JSONField(help_text='description of question')
    category = models.ManyToManyField(Category)
    type = models.CharField(max_length=2, choices=QuestionTypeChoice.choices, help_text='type of question')
    upvote = models.IntegerField(default=1, help_text='upvote of the question')
    downvote = models.IntegerField(default=1, help_text='downvote of the question')
    publish = models.BooleanField(default=1, help_text='publish the question or not')
    URL = models.URLField(max_length=20, blank=True, help_text='URL of question')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Keypoint(models.Model):
    name = models.CharField(max_length=50, help_text='name of the keypoint')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keypoint', blank=True, null=True)
    difficulty = models.IntegerField(default=1, help_text='difficulty of a keypoint')
    requirements = models.CharField(max_length=100, blank=True, help_text='requirements of keypoint')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

class Solution(models.Model):
    name = models.CharField(max_length=100, blank=True, help_text='solution name')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='solution_question')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='solution_category')
    answer = models.JSONField(help_text='detailed solution')
    keypoint = models.ManyToManyField(Keypoint)
    resources = models.JSONField(help_text='resources of question')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.question}'

class UserKeypointScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keypoint = models.ForeignKey(Keypoint, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class UserSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    keypoint = models.JSONField(blank=True, help_text='list of completed keypoint id')
    content = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
