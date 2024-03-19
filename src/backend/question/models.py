from django.db import models
from django.utils import timezone
from django.conf import settings


def get_default_json():
    return {}

class Milestone(models.Model):
    name = models.CharField(max_length=100, default='')
    step = models.CharField(default='implement', max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QTYPE = (
        (0, 'Choice'),
        (1, 'Coding'),
        (2, 'Voice'),
    )
    problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE)
    q_type = models.IntegerField(choices=QTYPE, default=0)
    tag = models.ManyToManyField('question.Tag')
    step = models.CharField(default='implement', max_length=1000)
    difficulty = models.IntegerField(default=100, help_text='percentage of difficulty')
    desc = models.JSONField(default=get_default_json)
    info = models.JSONField(default=get_default_json, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        desc_str = self.desc.get('desc', '') if isinstance(self.desc, dict) else ''
        return f"{self.problem.name} - {desc_str[:10]}"


class Tag(models.Model):
    category = models.CharField(max_length=100, default='algorithm')
    group = models.CharField(max_length=100, default='data-structure')
    name = models.CharField(max_length=100, default='Greedy')
    short_name = models.CharField(max_length=100, default='Grd')
    frequency = models.IntegerField(
        default=1, help_text='The larger the number, the higher the frequency')
    difficulty = models.IntegerField(
        default=1, help_text='The larger the number, the higher the difficulty')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class QuestionMilestone(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'milestone')

    def __str__(self):
        return f'{self.question.id} - {self.milestone.name}'
