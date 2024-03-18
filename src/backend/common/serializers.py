from django.contrib.auth import get_user_model
from rest_framework import serializers
from question.models import Tag
from .models import UserAbility, UserActivity

User = get_user_model()

class UserAbilitySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    tag_short_name = serializers.SerializerMethodField()  # Add this line
    tag_group = serializers.SerializerMethodField()

    class Meta:
        model = UserAbility
        fields = ['id', 'user', 'tag_short_name', 'tag_group', 'ability_score']  # Update this line

    def get_tag_short_name(self, obj):
        return obj.tag.short_name  # This method retrieves the short_name from the tag

    def get_tag_group(self, obj):  # Method to get the tag group
        return obj.tag.group


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'a_type', 'content', 'created_at', 'updated_at']
