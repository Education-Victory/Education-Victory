from django.contrib import admin
from .models import Question, Solution, Category


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Category, CategoryAdmin)
