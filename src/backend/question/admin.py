from django.contrib import admin
from .models import Solution, Category

class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')


admin.site.register(Solution, SolutionAdmin)
admin.site.register(Category, CategoryAdmin)
