from django.contrib import admin
from .models import Question, QuestionTopic

admin.site.register(Question)
admin.site.register(QuestionTopic)