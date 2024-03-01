from rest_framework import serializers
from .models import Problem, Milestone

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('name',)
