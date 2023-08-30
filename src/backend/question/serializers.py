import math
from rest_framework import serializers
from common.models import Task
from .models import Category, Solution, CodingQuestion, ChoiceQuestion


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'created_at', 'updated_at']


class SolutionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category_id.name', read_only=True)

    class Meta:
        model = Solution
        fields = ['id', 'category_name', 'created_at', 'updated_at']


class CodingQuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='solution_id.category_id.name', read_only=True)
    solution_name = serializers.CharField(source='solution_id.problem_id.name', read_only=True)
    qtype = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = ['id', 'name', 'diffculty', 'qtype', 'solution_name', 'category_name', 'created_at', 'updated_at']

    def get_qtype(self, obj):
        return 'Coding'


class ChoiceQuestionSerializer(serializers.ModelSerializer):
    solution = SolutionSerializer(read_only=True)
    qtype = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceQuestion
        fields = ['id', 'name', 'diffculty', 'qtype', 'solution', 'created_at', 'updated_at']


    def get_qtype(self, obj):
        return 'Choice'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'user_id', 'state', 'completeness', 'question_id_lists',
            'category', 'practice_method', 'content', 'created_at', 'updated_at']


