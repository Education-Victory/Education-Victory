from django.db import models
from django.utils import timezone

def get_default_json():
    return {}


class Problem(models.Model):
    CATEGORY_CHOICE = (
        ('algorithm', 'Algorithm'),
        ('system_design', 'System Design'),
        ('computer_science', 'Computer Science'),
        ('behavioral', 'Behavioral'),
        ('resume', 'Resume'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE, default='algorithm')
    desc = models.JSONField(default=get_default_json)
    upvote = models.IntegerField(default=1)
    downvote = models.IntegerField(default=1)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TagProblem(models.Model):
    tag = models.ForeignKey('question.Tag', on_delete=models.CASCADE)
    problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE)
    # The calculation method for the difficulty level of a tag for a specific Problem
    # is the maximum difficulty level among all the questions associated with that problem.
    difficulty = models.IntegerField(
        default=10, help_text='The larger the number, the higher the difficulty')
    weight = models.IntegerField(default=10)

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
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='onsite')
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    origin_link = models.URLField(max_length=1000, blank=True, help_text="URL for origin post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

