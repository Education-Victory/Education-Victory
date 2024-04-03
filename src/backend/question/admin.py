from django.contrib import admin
from .models import (
    Tag,
    Question,
    Milestone,
    QuestionMilestone
)

class QuestionMilestoneInline(admin.TabularInline):
    model = QuestionMilestone
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('desc', 'problem', 'step', 'difficulty', 'created_at', 'updated_at')
    list_filter = ('difficulty',)
    filter_horizontal = ('tag',)
    inlines = (QuestionMilestoneInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'group', 'frequency', 'difficulty', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'step', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'step')
