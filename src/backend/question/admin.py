from django.contrib import admin
from .models import Question, QuestionTopic, UserSubmission

admin.site.register(Question)
admin.site.register(QuestionTopic)
admin.site.register(UserSubmission)