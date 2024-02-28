import math
from rest_framework import serializers
from .models import CodingQuestion, ChoiceQuestion


class CodingQuestionBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodingQuestion
        fields = ['id', 'name', 'category', 'diffculty',
            'begin', 'during', 'finish', 'answer', 'text_hint', 'code_hint',
            'resource', 'created_at', 'updated_at']


class CodingQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodingQuestion
        fields = '__all__'



class ChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceQuestion
        fields = '__all__'
