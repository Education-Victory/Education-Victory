import math
from rest_framework import serializers
from .models import Question, Category, Solution, Keypoint

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'name', 'question', 'category', 'answer', 'keypoints',
                'resources', 'created_at', 'updated_at']

class KeypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keypoint
        fields = ['id', 'name', 'category', 'difficulty',
                'requirements', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'URL', 'solution_set', 'category', 'type',
                'created_at', 'updated_at']
