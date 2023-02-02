from rest_framework import serializers
from .models import WebUser

class WebUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['user', 'name', 'email', 'avatar']