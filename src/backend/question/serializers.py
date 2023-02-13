import math
from rest_framework import serializers
from .models import Question, Category

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
