from django.contrib.auth import get_user_model
from rest_framework import serializers
from question.models import Tag
from .models import UserAbility, UserActivity, UserSubmission

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
        fields = '__all__'


class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = '__all__'


class ReviewSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    q_type = serializers.IntegerField()
    content = serializers.CharField()
