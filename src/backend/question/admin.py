from django.template.defaultfilters import truncatewords
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
    list_display = ('get_short_desc', 'problem', 'step', 'difficulty', 'created_at', 'updated_at')
    list_filter = ('difficulty',)
    filter_horizontal = ('tag',)
    inlines = (QuestionMilestoneInline,)

    def get_short_desc(self, obj):
        """
        Returns the first 100 words of the description for display in the admin list.
        """
        return truncatewords(obj.desc, 20)  # Truncate to 100 words
    get_short_desc.short_description = 'Description'  # Sets column name


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'group', 'frequency', 'difficulty', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'step', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'step')
