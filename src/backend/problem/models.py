from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

def get_default_json():
    return {}

class Milestone(models.Model):
    name = models.CharField(max_length=100, default='')
    type = models.CharField(default='implement', max_length=1000)
    question = GenericRelation('MilestoneQuestion')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MilestoneQuestion(models.Model):
    milestone = models.ForeignKey('Milestone', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('milestone', 'content_type', 'object_id')

    def __str__(self):
        question_model_name = self.content_type.model_class().__name__
        question_desc = ""
        if hasattr(self.question, 'desc'):
            try:
                question_desc = self.question.desc.get('desc', '')[:20]
            except (TypeError, ValueError):
                question_desc = str(self.question.desc)[:20]
        milestone_name = self.milestone.name[:20] if self.milestone.name else ""
        return f'{milestone_name} + {question_model_name} + {question_desc}'


class Problem(models.Model):
    CATEGORY_CHOICE = (
        ('algorithm', 'Algorithm'),
        ('system design', 'System Design'),
        ('computer science', 'Computer Science'),
        ('behavioral', 'Behavioral'),
        ('resume', 'Resume'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE, default='algorithm')
    desc = models.JSONField(default=get_default_json)
    upvote = models.IntegerField(default=1)
    downvote = models.IntegerField(default=1)
    milestone = models.ManyToManyField(Milestone, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TagProblem(models.Model):
    tag = models.ForeignKey('question.Tag', on_delete=models.CASCADE)
    problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = [['tag', 'problem']]


class ProblemFrequency(models.Model):
    STAGE_CHOICES = (
        ('coding', 'Coding'),
        ('phone', 'Phone'),
        ('onsite', 'Onsite'),
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='frequency_problem')
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='onsite')
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    origin_link = models.URLField(max_length=1000, blank=True, help_text="URL for origin post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
