from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import WebUserCreationForm, WebUserChangeForm
from .models import WebUser, UserScore, UserFav

class WebUserAdmin(UserAdmin):
    add_form = WebUserCreationForm
    form = WebUserChangeForm
    model = WebUser
    list_display = ['email', 'username', 'avatar']

admin.site.register(WebUser, WebUserAdmin)
admin.register(UserScore)
admin.register(UserFav)

