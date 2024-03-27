import math
from rest_framework import serializers
from .models import Question, Milestone, Tag
from common.models import UserActivity



class MilestoneSerializer(serializers.ModelSerializer):
    state = serializers.BooleanField(read_only=True)

    class Meta:
        model = Milestone
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  # Adjust fields as necessary


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    question_name = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = '__all__'

    def get_question_name(self, obj):
        question = obj.type_of_question
        return str(question) if question else None
