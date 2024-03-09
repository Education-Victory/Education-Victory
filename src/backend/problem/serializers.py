from rest_framework import serializers
from .models import Problem, Milestone
from question.models import CodingQuestion, ChoiceQuestion
from question.serializers import CodingQuestionSerializer, ChoiceQuestionSerializer

class MilestoneSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = Milestone
        fields = '__all__'

    def get_question(self, obj):
        question_list = []
        for mq in obj.milestonequestion_set.all():
            question_instance = mq.question
            if question_instance:
                serializer_class = self.get_serializer_class_for_model(
                    type(question_instance))
                if serializer_class:
                    serializer = serializer_class(
                        instance=question_instance, context=self.context)
                    question_list.append(serializer.data)
        return question_list


    def get_serializer_class_for_model(self, model_class):
        serializer_mapping = {
            CodingQuestion: CodingQuestionSerializer,
            ChoiceQuestion: ChoiceQuestionSerializer,
        }
        return serializer_mapping.get(model_class, None)


class ProblemSerializer(serializers.ModelSerializer):
    milestone_detail = MilestoneSerializer(
        source='milestone', many=True, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
