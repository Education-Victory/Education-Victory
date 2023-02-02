from django.contrib import admin
from .models import Question, Keypoint, Question_Keypoint_Mapping, User_Keypoint_Score, UserSubmission, Solution

admin.site.register(Question)
admin.site.register(Keypoint)
admin.site.register(Question_Keypoint_Mapping)
admin.site.register(User_Keypoint_Score)
admin.site.register(UserSubmission)
admin.site.register(Solution)
