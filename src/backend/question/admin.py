from django.contrib import admin
from .models import (
    Tag,
    CodingQuestion,
    TagCoding,
    ChoiceQuestion,
    TagChoice,
    UserSubmission,
    TestCase,
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'difficulty', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ('desc', 'problem', 'difficulty', 'created_at', 'updated_at')
    list_filter = ('difficulty',)
    search_fields = ('desc', 'default_code')

@admin.register(TagCoding)
class TagCodingAdmin(admin.ModelAdmin):
    list_display = ('tag', 'coding_question', 'weight')
    list_filter = ('tag',)

@admin.register(ChoiceQuestion)
class ChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('desc', 'problem', 'type', 'difficulty', 'created_at', 'updated_at')
    list_filter = ('type', 'difficulty')
    search_fields = ('desc',)

@admin.register(TagChoice)
class TagChoiceAdmin(admin.ModelAdmin):
    list_display = ('tag', 'choice_question', 'weight')
    list_filter = ('tag',)

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'milestone', 'created_at', 'updated_at')
    list_filter = ('content_type', 'user')

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('coding_question', 'case_input', 'case_output', 'created_at', 'updated_at')
    search_fields = ('coding_question__desc',)
