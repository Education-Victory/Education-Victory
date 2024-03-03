import math
from rest_framework import serializers
from .models import CodingQuestion, ChoiceQuestion, UserSubmission


class CodingQuestionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = '__all__'

    def get_name(self, obj):
        return str(obj)


class ChoiceQuestionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceQuestion
        fields = '__all__'

    def get_name(self, obj):
        return str(obj)


class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = '__all__'
