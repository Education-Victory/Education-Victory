from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import WebUser

class WebUserCreationForm(UserCreationForm):

    class Meta:
        model = WebUser
        fields = ('username', 'email','avatar')

class WebUserChangeForm(UserChangeForm):

    class Meta:
        model = WebUser
        fields = ('username', 'email', 'avatar')