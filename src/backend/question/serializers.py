import math
from rest_framework import serializers
from .models import CodingQuestion, ChoiceQuestion


class CodingQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodingQuestion
        fields = '__all__'

class ChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceQuestion
        fields = '__all__'
