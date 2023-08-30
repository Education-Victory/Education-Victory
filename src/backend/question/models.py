from uu import Error
from django.db import models
from django.utils import timezone
from django.conf import settings


def get_default_json():
    return '{}'

class Category(models.Model):
    topic = models.CharField(max_length=100, help_text='topic of category')
    group = models.CharField(max_length=100, help_text='group of category')
    name = models.CharField(max_length=100)
    weight = models.IntegerField(default=1, help_text='bigger means more important')
    diffculty = models.IntegerField(default=1, help_text='diffculty of the category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


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
    name = models.CharField(blank=True, max_length=100)
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='solution_problem')
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='solution_category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.problem_id.name} - {self.category_id.name}'


class CodingQuestion(models.Model):
    name = models.CharField(blank=True, max_length=100)
    solution_id = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='coding_question_solution')
    description = models.CharField(max_length=4000)
    diffculty = models.IntegerField(default=0)
    solution = models.CharField(blank=True, max_length=4000)
    text_hint = models.JSONField(default=get_default_json)
    code_hint = models.CharField(blank=True, max_length=4000)
    resource = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChoiceQuestion(models.Model):
    name = models.CharField(blank=True, max_length=100)
    solution_id = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='choice_question_solution')
    description = models.CharField(max_length=2000)
    answer_number = models.IntegerField(default=1)
    diffculty = models.IntegerField(default=0)
    choice = models.JSONField(default=get_default_json)
    solution = models.CharField(max_length=100, help_text='binary form of the correct answer')
    text_hint = models.JSONField(default=get_default_json)
    resource = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    coding_question_id = models.ForeignKey(
        CodingQuestion, on_delete=models.CASCADE, related_name='testcase_coding_question')
    case_input = models.JSONField(default=get_default_json)
    case_output = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
