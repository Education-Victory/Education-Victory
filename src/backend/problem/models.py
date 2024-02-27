from django.db import models
from django.utils import timezone

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
    description = models.CharField(max_length=4000)
    upvote = models.IntegerField(default=1)
    downvote = models.IntegerField(default=1)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
