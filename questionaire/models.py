from django.db import models

# Create your models here.

class Questionaire(models.Model):
    theme = models.CharField(max_length=100)
    
class QuestionaireQuestion(models.Model):
    description = models.TextField()
    theme = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    
class QuestionaireOption(models.Model):
    question = models.ForeignKey(QuestionaireQuestion, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)

class QuestionaireSubmission(models.Model):
    question = models.ForeignKey(QuestionaireQuestion, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(QuestionaireOption, on_delete=models.CASCADE)
    # submit_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # TODO: link to an user 
    
    
    
    