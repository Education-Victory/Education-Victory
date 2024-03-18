import math
from rest_framework import serializers
from .models import Question, Milestone
from common.models import UserActivity



class MilestoneSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = Milestone
        fields = '__all__'

    def get_question(self, obj):
        question_list = []
        for mq in obj.milestonequestion_set.all():
            return []

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  # Adjust fields as necessary


class UserActivitySerializer(serializers.ModelSerializer):
    question_name = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = '__all__'

    def get_question_name(self, obj):
        question = obj.type_of_question
        return str(question) if question else None
