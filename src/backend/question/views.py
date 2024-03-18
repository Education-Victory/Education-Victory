import urllib.parse
from datetime import timedelta
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from problem.models import Problem, TagProblem
from .models import Question, Tag
from common.models import UserActivity
from .serializers import QuestionSerializer
from common.serializers import UserActivitySerializer


LAST_YEAR = timezone.now() - timedelta(days=365)


class QuestionViewSet(viewsets.ViewSet):
    pass


class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer

    @action(detail=False, methods=['post'], url_path='submit-answer')
    def submit_answer(self, request, *args, **kwargs):
        pass


def update_tag_problem_difficulty(problem, tag):
    questions_with_tag = Question.objects.filter(problem=problem, tag=tag)

    if questions_with_tag.exists():
        # If there are questions associated with the tag, find the highest difficulty.
        highest_difficulty = 0
        for question in questions_with_tag:
            question_difficulty = question.difficulty * tag.difficulty
            highest_difficulty = max(highest_difficulty, question_difficulty)

        # Update the TagProblem instance with the new highest difficulty.
        TagProblem.objects.update_or_create(
            tag=tag,
            problem=problem,
            defaults={'difficulty': highest_difficulty}
        )
    else:
        # If no questions are associated with this tag for the problem, remove the TagProblem instance.
        TagProblem.objects.filter(tag=tag, problem=problem).delete()


@receiver(m2m_changed, sender=Question.tag.through)
def update_tag_problem(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        problem = instance.problem
        if action == "post_clear":
            tags = problem.tags.all()
        else:
            tags = kwargs.get('model', Tag).objects.filter(pk__in=kwargs.get('pk_set', []))
        for tag in tags:
            update_tag_problem_difficulty(problem, tag)
