from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from problem.models import Problem


def get_default_json():
    return {}


class Tag(models.Model):
    name = models.CharField(max_length=100, default='greedy')
    weight = models.IntegerField(default=1, help_text='bigger means more important')
    difficulty = models.IntegerField(default=1, help_text='bigger means more difficult')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Checklist(models.Model):
    name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class CodingQuestion(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, through='TagCoding')
    desc = models.models.JSONField(default=get_default_json)
    default_code = models.TextField(max_length=4000)
    difficulty = models.IntegerField(default=0)
    answer = models.CharField(blank=True, max_length=8000)
    checklist = models.ManyToManyField(Checklist)
    text_hint = models.CharField(blank=True, max_length=1000)
    text_hint_2 = models.CharField(blank=True, max_length=1000)
    code_hint = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc[:50]


class TagCoding(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    coding_question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = [['tag', 'coding_question']]


class ChoiceQuestion(models.Model):
    TYPE = (
        (0, 'Single'),
        (1, 'Multiple'),
    )

    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, through='TagChoice')
    desc = models.JSONField(default=get_default_json)
    type = models.IntegerField(choices=TYPE, default=0)
    difficulty = models.IntegerField(default=0)
    choice = models.JSONField(default=get_default_json)
    answer = models.IntegerField(default=1, help_text='binary form of the correct answer')
    checklist = models.ManyToManyField(Checklist)
    text_hint = models.CharField(blank=True, max_length=1000)
    text_hint_2 = models.CharField(blank=True, max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class TagChoice(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    choice_question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = [['tag', 'choice_question']]


class UserSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    type_of_question = GenericForeignKey('content_type', 'object_id')
    checklist = models.IntegerField(default=1, help_text='binary form of checked checklist')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class TestCase(models.Model):
    coding_question = models.ForeignKey(
        CodingQuestion, on_delete=models.CASCADE)
    case_input = models.JSONField(default=get_default_json)
    case_output = models.JSONField(default=get_default_json)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
