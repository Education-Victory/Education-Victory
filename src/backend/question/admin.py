from django.contrib import admin
from .models import Question, Keypoint, UserKeypointScore, UserSubmission, Solution, Category

admin.site.register(Question)
admin.site.register(Keypoint)
admin.site.register(UserKeypointScore)
admin.site.register(UserSubmission)
admin.site.register(Solution)
admin.site.register(Category)
