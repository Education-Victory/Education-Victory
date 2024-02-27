from django.contrib import admin
from .models import Problem, ProblemFrequency

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'upvote', 'downvote', 'is_published', 'created_at', 'updated_at')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')

@admin.register(ProblemFrequency)
class ProblemFrequencyAdmin(admin.ModelAdmin):
    list_display = ('problem', 'stage', 'company', 'location', 'created_at', 'updated_at')
    list_filter = ('stage', 'company', 'location')
    search_fields = ('problem__name', 'company')
