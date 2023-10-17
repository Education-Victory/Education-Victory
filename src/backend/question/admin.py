from django.contrib import admin
from .models import Category, Problem, CodingQuestion, ChoiceQuestion


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'group', 'name', 'diffculty')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'diffculty')


class ChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'diffculty')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
