from django.contrib import admin
from .models import UserSubmission

class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

admin.site.register(UserSubmission, UserSubmissionAdmin)
