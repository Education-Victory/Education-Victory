from django.contrib import admin
from .models import User, Company, UserAbility, UserActivity, UserSubmission

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_premium', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_superuser', 'is_premium')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'resource', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserAbility)
class UserAbilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'ability_score')  # Columns to display in the admin list view
    list_filter = ('user', 'tag')  # Filters on the right sidebar
    search_fields = ('user__username', 'tag__name')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'a_type', 'created_at', 'updated_at')
    list_filter = ('user', 'a_type')

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'problem_id', 'question_id', 'created_at', 'updated_at')
    list_filter = ('user_id', 'problem_id', 'question_id')
