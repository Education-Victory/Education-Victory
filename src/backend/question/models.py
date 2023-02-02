from django.db import models


class QuestionCategory(models.Model):
    category = models.CharField(
        max_length=20, help_text="Category of a question")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Categroy"
        verbose_name_plural = "Categories"


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

    name = models.CharField(max_length=100, blank=True,
                            help_text="Question Name(Optional)")
    description = models.TextField(
        max_length=200, blank=True, help_text="Detailed Description of Question(Optional)")
    url = models.URLField(max_length=20, blank=True,
                          null=True, help_text="URL source of question")
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    type = models.CharField(
        max_length=2, choices=QuestionTypeChoice.choices, help_text="Type of question")
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    followUp = models.JSONField(
        blank=True, null=True, help_text="follow-up of question")
    resource = models.JSONField(
        blank=True, null=True, help_text="resource to study for this question")
    choice = models.JSONField(blank=True, null=True,
                              help_text="multiple choices")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solution = models.TextField(help_text="Solution to a specified question")

    def __str__(self):
        return f"{self.question} - {self.solution}"


class Keypoint(models.Model):
    difficulty = models.IntegerField(
        default=1, help_text="Difficulty of a keypoint")
    name = models.CharField(max_length=50, help_text="Name of the keypoint")
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    requirements = models.JSONField(
        blank=True, null=True, help_text="requirements of a keypoint")

    def __str__(self):
        return f"{self.category} - {self.name}"


class Question_Keypoint_Mapping(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    keypoint = models.ForeignKey(Keypoint, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question} - {self.keypoint}"


class User_Keypoint_Score(models.Model):
    # TODO: foreign keys : user id
    keypoint = models.ForeignKey(Keypoint, on_delete=models.CASCADE)
    score = models.FloatField()


class UserSubmission(models.Model):
    # TODO: foreign keys : user id
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    content = models.JSONField(blank=True, null=True)
    completeness = models.JSONField(blank=True, null=True)
    points = models.FloatField(help_text="score added by this submission")