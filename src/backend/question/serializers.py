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
    question_name = serializers.SerializerMethodField()

    class Meta:
        model = UserSubmission
        fields = '__all__'

    def get_question_name(self, obj):
        question = obj.type_of_question
        return str(question) if question else None
