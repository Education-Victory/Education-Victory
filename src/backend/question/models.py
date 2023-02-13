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

    name = models.CharField(max_length=100, blank=True,
                            help_text="Question Name(Optional)")
    description = models.JSONField(
        help_text="Detailed Description of Question")
    url = models.URLField(max_length=20, blank=True,
                          null=True, help_text="URL source of question")
    type = models.CharField(
        max_length=2, choices=QuestionTypeChoice.choices, help_text="Type of question")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField(
        help_text="detailed solution", default={"solutions": ""})
    # follow up for similar questions/mutated versions, resources for better understanding
    followUp = models.JSONField(
        default={"followup": [], "resources": []}, help_text="follow-up of question")
    keypoints = models.JSONField(
        default={"keypoints": []}, help_text="list of keypoints'id")

    def __str__(self):
        return f"{self.question} - {self.pk}"


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=30, default="question category")


class Keypoint(models.Model):
    difficulty = models.IntegerField(
        default=1, help_text="Difficulty of a keypoint")
    name = models.CharField(max_length=50, help_text="Name of the keypoint")
    requirements = models.JSONField(
        blank=True, null=True, help_text="requirements of a keypoint")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class UserKeypointScore(models.Model):
    # TODO: foreign keys : user id
    keypoint = models.ForeignKey(Keypoint, on_delete=models.CASCADE)
    score = models.FloatField()


class UserSubmission(models.Model):
    # TODO: foreign keys : user id
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True)
    content = models.JSONField(blank=True, null=True)
    # same fields in Keypoint's requirements
    completeness = models.JSONField(blank=True, null=True)
    points = models.FloatField(
        help_text="score added by this submission", default=0.0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
