from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from .models import Problem, TagProblem, ProblemFrequency, Milestone, MilestoneQuestion


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


class MilestoneAdmin(admin.ModelAdmin):
    readonly_fields = ['related_questions_summary']

    def related_questions_summary(self, obj):
        # Fetching all related MilestoneQuestion objects
        related_questions = obj.milestonequestion_set.all()
        if related_questions:
            # Building a HTML list of related questions for display
            questions_list = ''.join([f'<li>{str(question)}</li>' for question in related_questions])
            return format_html(f'<ul>{questions_list}</ul>')
        return "No questions linked"
    related_questions_summary.short_description = "Related Questions"

admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(MilestoneQuestion)
