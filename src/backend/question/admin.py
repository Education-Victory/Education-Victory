from django.contrib import admin
from .models import Category, Problem, Solution, CodingQuestion, ChoiceQuestion


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'group', 'name', 'diffculty')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'diffculty')


class ChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'diffculty')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
