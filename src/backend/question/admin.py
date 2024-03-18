from django.contrib import admin
from .models import (
    Tag,
    Question,
)
from common.models import UserActivity

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('desc', 'problem', 'step', 'difficulty', 'created_at', 'updated_at')
    list_filter = ('difficulty',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'frequency', 'difficulty', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'a_type', 'created_at', 'updated_at')
    list_filter = ('user', 'a_type')
