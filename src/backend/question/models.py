from uu import Error
from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=30, help_text='category of solution')
    weight = models.IntegerField(default=1, help_text='weight of the category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):

    name = models.CharField(max_length=100, blank=True,
                            help_text='question name')
    description = models.JSONField(help_text='description of question')
    category_id_list = models.ManyToManyField(Category)
    upvote = models.IntegerField(default=1, help_text='upvote of the question')
    downvote = models.IntegerField(
        default=1, help_text='downvote of the question')
    publish = models.BooleanField(
        default=1, help_text='publish the question or not')
    URL = models.URLField(max_length=20, blank=True,
                          help_text='URL of question')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Keypoint(models.Model):
    name = models.CharField(max_length=50, help_text='name of the keypoint')
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='keypoint', blank=True, null=True)
    difficulty = models.IntegerField(
        default=1, help_text='difficulty of a keypoint')
    requirements = models.CharField(
        max_length=100, blank=True, help_text='requirements of keypoint')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Ability(models.Model):
    ability: models.JSONField(default=dict, blank=True)

    # Sanity check on save
    def clean(self, new_default=0):
        for key in self.data.keys():
            if key not in settings.VALID_ABILITY_KEYS:
                raise Error(f"Invalid key: {key}")
        # Set default value to new added keys
        for key in settings.VALID_ABILITY_KEYS:
            if key not in self.data.keys():
                self.data[key] = 0

    # Initialize when no value is supported

    def save(self, *args, **kwargs):
        # Initialize if not defined
        if not self.data:
            self.data = {key: 0 for key in settings.VALID_ABILITY_KEYS}
        self.full_clean()
        super().save(*args, **kwargs)


class Solution(models.Model):
    class SolutionType(models.TextChoices):
        CODING = 'CO', 'Coding'
        CHOICE = 'CH', 'Choice'

    type = models.CharField(
        max_length=2, choices=SolutionType.choices, help_text='required solution type', null=True)

    name = models.CharField(max_length=100, blank=True,
                            help_text='solution name')
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='solution_question')
    category_id_list = models.ManyToManyField(Category)
    answer = models.JSONField(help_text='detailed solution')
    keypoint = models.ManyToManyField(Keypoint)
    resources = models.JSONField(help_text='resources of question')
    ability_id = models.ForeignKey(
        Ability, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.question}'


class UserKeypointScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    keypoint = models.ForeignKey(Keypoint, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
