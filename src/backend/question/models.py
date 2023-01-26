from django.db import models


class Question(models.Model):
    class QuestionTypeChoice(models.TextChoices):
        # Choices for types of a question
        MULTIPLE_CHOICE = "MC", "Multiple Choice"
        SHORT_ANSWER = "SA", "Short Answer"
        TRUE_O_FALSE = "TF", "True / False"
        CODE = "CO", "Code"

    class QuestionCategoryChoice(models.TextChoices):
        # Choices for category of a question
        QUIZ = "QZ", "Quiz"
        MOCK = "MK", "Mock"
        PRACTICE = "PR", "Practice"

    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=200, blank=True)
    url = models.URLField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=2, choices=QuestionTypeChoice.choices)
    category = models.CharField(
        max_length=2, choices=QuestionCategoryChoice.choices, blank=True)
    difficulty = models.JSONField(blank=True, null=True)
    requirement = models.JSONField(blank=True, null=True)
    hint = models.JSONField(blank=True, null=True)
    followUp = models.JSONField(blank=True, null=True)
    resource = models.JSONField(blank=True, null=True)
    choice = models.JSONField(blank=True, null=True)
    answer = models.JSONField(blank=True, null=True)
    label = models.JSONField(blank=True, null=True)


class QuestionTopic(models.Model):
    topic = models.CharField(max_length=20)
    
class UserSubmission(models.Model):
    # TODO: foreign keys : user id 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    content = models.JSONField(blank=True, null=True)
    completeness = models.JSONField(blank=True, null=True)