from uu import Error
from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    topic = models.CharField(max_length=100, help_text='topic of category')
    group = models.CharField(max_length=100, help_text='group of category')
    name = models.CharField(max_length=100)
    weight = models.IntegerField(default=1, help_text='bigger means more important')
    diffculty = models.IntegerField(default=1, help_text='diffculty of the category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.topic} - {self.group} - {self.name}'


class Problem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    category_id_list = models.ManyToManyField(Category)
    upvote = models.IntegerField(default=1)
    downvote = models.IntegerField(default=1)
    is_published = models.BooleanField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Solution(models.Model):
    name = models.CharField(max_length=100)
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='solution_problem')
    category_id_list = models.ManyToManyField(Category)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CodingQuestion(models.Model):
    name = models.CharField(max_length=100)
    solution_id = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='coding_question_solution')
    description = models.CharField(max_length=4000)
    diffculty = models.JSONField()
    solution = models.CharField(max_length=4000)
    text_hint = models.JSONField()
    code_hint = models.CharField(max_length=4000)
    resource = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ChoiceQuestion(models.Model):
    name = models.CharField(max_length=100)
    solution_id = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='choice_question_solution')
    description = models.CharField(max_length=2000)
    answer_number = models.IntegerField(default=1)
    diffculty = models.JSONField()
    choice = models.JSONField()
    solution = models.CharField(max_length=100, help_text='binary form of the correct answer')
    text_hint = models.JSONField()
    resource = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    coding_question_id = models.ForeignKey(
        CodingQuestion, on_delete=models.CASCADE, related_name='testcase_coding_question')
    case_input = models.JSONField()
    case_output = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
