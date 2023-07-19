from uu import Error
from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=30, help_text='category of question/solution')
    weight = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.JSONField(blank=True)
    ide_description = models.JSONField(blank=True, help_text='default description/code in the IDE')
    category_id_list = models.ManyToManyField(
        Category, help_text='category list related to question based on its solution')
    upvote = models.IntegerField(default=1)
    downvote = models.IntegerField(default=1)
    publish = models.BooleanField(default=1, help_text='publish the question or not')
    URL = models.URLField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='testcase_question')
    input = models.JSONField(help_text='JSON: {array: [1,2,3], target: 10}')
    output = models.JSONField(help_text='JSON: {result: [0,1]}')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Solution(models.Model):
    class Type(models.TextChoices):
        CODING = 'CO', 'Coding'
        CHOICE = 'CH', 'Choice'

    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=2, choices=Type.choices, help_text='solution type')
    description = models.JSONField(help_text='text in the IDE')
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='solution_question')
    category_id_list = models.ManyToManyField(Category)
    ability = models.JSONField()
    resources = models.JSONField(help_text='resources of question')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.question}'
