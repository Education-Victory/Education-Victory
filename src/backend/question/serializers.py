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
    qtype = serializers.SerializerMethodField()
    frequency = serializers.SerializerMethodField()
    total_frequency = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = ['id', 'name', 'category', 'frequency',
            'total_frequency', 'diffculty', 'qtype', 'created_at', 'updated_at']

    def get_qtype(self, obj):
        return 'Coding'

    def get_frequency(self, obj):
        return obj.frequency

    def get_total_frequency(self, obj):
        return obj.total_frequency


class ChoiceQuestionSerializer(serializers.ModelSerializer):
    qtype = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceQuestion
        fields = ['id', 'name', 'category', 'diffculty', 'qtype', 'created_at', 'updated_at']


    def get_qtype(self, obj):
        return 'Choice'
