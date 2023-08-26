import math
from rest_framework import serializers
from common.models import Task
from .models import Category, Solution


class SolutionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'category_name', 'created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.name

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight', 'created_at', 'updated_at']


class BasicTaskSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    method = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'user_id', 'question_id_lists',
            'practice_method', 'content', 'created_at', 'updated_at']


