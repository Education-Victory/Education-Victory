from django.contrib import admin
from .models import Question, Keypoint, UserKeypointScore, Solution, Category


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class KeypointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_id')


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Keypoint, KeypointAdmin)
admin.site.register(UserKeypointScore)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Category, CategoryAdmin)
