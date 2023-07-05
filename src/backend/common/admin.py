from django.contrib import admin
from .models import UserSubmission

class UserSubmissionAdmin(admin.ModelAdmin):
    # Sets 'id' and 'user' fields to be displayed on the UserSubmission admin list view,
    list_display = ('id', 'user_id')

admin.site.register(UserSubmission, UserSubmissionAdmin)
