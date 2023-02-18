import math
from rest_framework import serializers
from .models import Question, Category, Solution, Keypoint

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'URL', 'type',
                'created_at', 'updated_at']

class KeypointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keypoint
        fields = ['id', 'name', 'category', 'difficulty',
                'requirements', 'created_at', 'updated_at']

class SolutionSerializer(serializers.ModelSerializer):
    keypoint = KeypointSerializer(many=True, read_only=True)
    question_name = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'name', 'question_name', 'category', 'answer', 'keypoint',
                'resources', 'created_at', 'updated_at']

    def get_question_name(self, obj):
        return obj.question.name

class CategorySerializer(serializers.ModelSerializer):
    keypoint = KeypointSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'keypoint', 'created_at', 'updated_at']


