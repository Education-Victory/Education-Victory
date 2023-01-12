from django.db import models

# Create your models here.
class Quiz(models.Model):
    # model for Quiz
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        
    def __str__(self):
        return self.name 
    
class QuizQuestion(models.Model):
    # model for quiz question
    question = models.TextField(max_length=500)
    belong_to_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.belong_to_quiz} - {self.question}"

class QuestionOption(models.Model):
    # model for question options 
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question} - {self.option}"

class QuizSubmission(models.Model):
    # model for quiz submission 
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING) 
    score = models.IntegerField(default=0)
    # TODO: a property for the user
    
    def __str__(self):
        return f"{self.quiz} - {self.score}"
    


