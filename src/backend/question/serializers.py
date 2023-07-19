import math
from rest_framework import serializers
from .models import Question, Category, Solution

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'URL', 'type',
                'created_at', 'updated_at']

class SolutionSerializer(serializers.ModelSerializer):
    question_name = serializers.SerializerMethodField()
    question_des = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'name', 'question_name', 'question_des', 'category_name', 'category', 'answer',
                'resources', 'created_at', 'updated_at']

    def get_question_name(self, obj):
        return obj.question.name

    def get_question_des(self, obj):
        return obj.question.description

    def get_category_name(self, obj):
        return obj.category.name

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'created_at', 'updated_at']


