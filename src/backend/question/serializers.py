import math
from rest_framework import serializers
from common.models import Task
from .models import Category, CodingQuestion, ChoiceQuestion


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'created_at', 'updated_at']


class CodingQuestionSerializer(serializers.ModelSerializer):
    qtype = serializers.SerializerMethodField()
    frequency = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = ['id', 'name', 'category', 'frequency', 'diffculty', 'qtype', 'created_at', 'updated_at']

    def get_qtype(self, obj):
        return 'Coding'

    def get_frequency(self, obj):
        return obj.frequency


class ChoiceQuestionSerializer(serializers.ModelSerializer):
    qtype = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceQuestion
        fields = ['id', 'name', 'category', 'diffculty', 'qtype', 'created_at', 'updated_at']


    def get_qtype(self, obj):
        return 'Choice'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'user_id', 'state', 'completeness', 'question_id_lists',
            'category', 'practice_method', 'content', 'created_at', 'updated_at']


