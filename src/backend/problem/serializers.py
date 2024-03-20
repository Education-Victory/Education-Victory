from rest_framework import serializers
from .models import Problem, TagProblem
from common.models import UserAbility
from question.models import Question
from question.serializers import QuestionSerializer, TagSerializer


class ProblemSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'  # Adjust this to include specific fields as necessary

    def get_questions(self, obj):
        problem = obj['problem'] if isinstance(obj, dict) else obj
        organized_questions = {}
        questions = problem.question_set.all().order_by('step')
        for question in questions:
            if question.step not in organized_questions:
                organized_questions[question.step] = []
            organized_questions[question.step].append(QuestionSerializer(question).data)
        return organized_questions


class CustomProblemSerializer(serializers.Serializer):
    problem = ProblemSerializer()
    tag = TagSerializer()
    user_ability = serializers.IntegerField()
    tag_difficulty = serializers.IntegerField()
