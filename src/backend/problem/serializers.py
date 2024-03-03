from rest_framework import serializers
from .models import Problem, Milestone

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    milestone_detail = MilestoneSerializer(source='milestone', many=True, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('name',)
