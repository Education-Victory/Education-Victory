from rest_framework import serializers
from .models import Problem, Milestone

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    milestone_name = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_milestone_name(self, obj):
        return [milestone.name for milestone in obj.milestone.all()]


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('name',)
