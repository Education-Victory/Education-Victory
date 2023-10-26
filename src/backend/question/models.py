from uu import Error
from django.db import models
from django.utils import timezone
from django.conf import settings


def get_default_json():
    return '{}'


class Category(models.Model):
    topic = models.CharField(max_length=100, default='algorithm', help_text='topic of category')
    group = models.CharField(max_length=100, default='greedy', help_text='group of category')
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


class CodingQuestion(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='coding_question_problem')
    name = models.CharField(blank=True, max_length=100)
    category = models.CharField(blank=True, max_length=100)
    begin = models.TextField(max_length=4000)
    during = models.TextField(max_length=4000)
    finish = models.TextField(max_length=4000)
    description = models.TextField(max_length=4000)
    diffculty = models.IntegerField(default=0)
    answer = models.CharField(blank=True, max_length=4000)
    text_hint = models.JSONField(default=get_default_json)
    code_hint = models.CharField(blank=True, max_length=4000)
    resource = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ChoiceQuestion(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='choice_question_problem')
    name = models.CharField(blank=True, max_length=100)
    category = models.CharField(blank=True, max_length=100)
    description = models.CharField(max_length=2000)
    answer_number = models.IntegerField(default=1)
    diffculty = models.IntegerField(default=0)
    choice = models.JSONField(default=get_default_json)
    answer = models.CharField(max_length=100, help_text='binary form of the correct answer')
    text_hint = models.JSONField(default=get_default_json)
    resource = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    coding_question = models.ForeignKey(
        CodingQuestion, on_delete=models.CASCADE, related_name='testcase_coding_question')
    case_input = models.JSONField(default=get_default_json)
    case_output = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemFrequency(models.Model):
    STAGE_CHOICES = (
        ('coding', 'Coding'),
        ('phone', 'Phone'),
        ('onsite', 'Onsite'),
    )
    QTYPE_CHOICES = (
        ('algorithm', 'Algorithm'),
        ('computer science', 'Computer Science'),
        ('system design', 'System Design'),
        ('behavioral', 'Behavioral'),
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='frequency_problem')
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='onsite')
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    origin_link = models.URLField(max_length=1000, blank=True, help_text="URL for origin post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
