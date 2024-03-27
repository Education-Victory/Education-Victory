from rest_framework import serializers
from .models import Problem, TagProblem
from common.models import UserAbility
from question.models import Question, Milestone, QuestionMilestone
from question.serializers import QuestionSerializer, TagSerializer, MilestoneSerializer


class ProblemSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    milestones = serializers.SerializerMethodField()

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

    def get_milestones(self, obj):
        user = self.context.get('request').user
        problem = obj
        milestones = Milestone.objects.filter(question__problem=problem).distinct()
        milestones_data = {}
        completed_milestones = 0

        for milestone in milestones:
            related_questions = QuestionMilestone.objects.filter(
                milestone=milestone, question__problem=problem, user=user)
            total_questions = related_questions.count()
            completed_questions = related_questions.filter(state=True).count()

            # A milestone is considered completed if all its related questions have state=True
            is_milestone_completed = (total_questions == completed_questions and total_questions > 0)
            if is_milestone_completed:
                completed_milestones += 1

            milestones_data[milestone.id] = {
                "milestone": MilestoneSerializer(milestone).data,
                "state": is_milestone_completed
            }

        total_milestones = milestones.count()
        milestone_completeness = (completed_milestones // total_milestones * 100) if total_milestones else 0

        # Add the milestone_completeness to each milestone data
        for milestone_data in milestones_data.values():
            milestone_data["milestone"]['milestone_completeness'] = milestone_completeness

        return [milestone_data["milestone"] for milestone_data in milestones_data.values()]


class CustomProblemSerializer(serializers.Serializer):
    problem = ProblemSerializer()
    tag = TagSerializer()
    user_ability = serializers.IntegerField()
    tag_difficulty = serializers.IntegerField()
