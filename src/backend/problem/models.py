from django.db import models
from django.utils import timezone
from question.models import Tag

def get_default_json():
    return {}


class Problem(models.Model):
    CATEGORY_CHOICE = (
        ('Algorithm', 'Algorithm'),
        ('System Design', 'System Design'),
        ('Computer Science', 'Computer Science'),
        ('Behavioral', 'Behavioral'),
        ('Resume', 'Resume'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE, default='Algorithm')
    tags = models.ManyToManyField(Tag, through='TagProblem')
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
        ('phone', 'Phone'),
        ('onsite', 'Onsite'),
    )
    POSITION_TYPE = (
        ('swe', 'Software Engineer'),
        ('fe', 'Frontend Engineer'),
        ('mle', 'Machine Learning Engineer'),
        ('ds', 'Data Scientist'),
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='frequency_problem')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='onsite')
    position_type = models.CharField(max_length=20, choices=POSITION_TYPE, default='swe')
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    origin_content = models.CharField(max_length=4000, blank=True)
    origin_link = models.URLField(max_length=1000, blank=True, help_text="URL for origin post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemCompany(models.Model):
    problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE)
    company = models.ForeignKey('common.Company', on_delete=models.CASCADE)
    popularity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('problem', 'company')  # Ensures uniqueness for each problem-company pair

    def __str__(self):
        return f"{self.problem.name} - {self.company.name} ({self.popularity})"
