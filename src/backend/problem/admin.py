from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from .models import Problem, TagProblem, ProblemFrequency


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
    list_display = ('problem', 'company', 'location', 'created_at')
    list_filter = ('company', 'location')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

