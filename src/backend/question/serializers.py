import math
from rest_framework import serializers
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


