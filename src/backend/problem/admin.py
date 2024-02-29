from django.contrib import admin
from .models import Problem, TagProblem, ProblemFrequency, Checklist

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'category')
    search_fields = ('name', 'category')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(TagProblem)
class TagProblemAdmin(admin.ModelAdmin):
    list_display = ('tag', 'problem', 'weight')
    list_filter = ('tag',)
    search_fields = ('tag__name', 'problem__name')


@admin.register(ProblemFrequency)
class ProblemFrequencyAdmin(admin.ModelAdmin):
    list_display = ('problem', 'stage', 'company', 'location', 'created_at')
    list_filter = ('stage', 'company', 'location')
    search_fields = ('problem__name', 'company', 'location')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
