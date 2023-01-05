from django.db import models

# Create your models here.
class CodeQuestionItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
