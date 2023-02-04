from rest_framework import serializers
from .models import WebUser, UserScore, UserFav

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = '__all__'

class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = '__all__'

class UserFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFav
        fields = '__all__' 