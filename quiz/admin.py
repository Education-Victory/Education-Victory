from django.contrib import admin

# Register your models here.
from .models import Quiz, QuizQuestion, QuestionOption, QuizSubmission
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuestionOption)
admin.site.register(QuizSubmission)

