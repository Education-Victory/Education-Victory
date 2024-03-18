from rest_framework import serializers
from .models import Problem
from question.models import Question
from question.serializers import QuestionSerializer



class ProblemSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_questions(self, obj):
        organized_questions = {}
        questions = obj.question_set.all().order_by('step')
        for question in questions:
            if question.step not in organized_questions:
                organized_questions[question.step] = []
            organized_questions[question.step].append(QuestionSerializer(question).data)
        return organized_questions
