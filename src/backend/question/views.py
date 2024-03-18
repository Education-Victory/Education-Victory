import urllib.parse
from datetime import timedelta
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from problem.models import Problem, TagProblem
from .models import Question, TagQuestion
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


@receiver(post_save, sender=Question)
def update_tag_problem_difficulty(sender, instance, **kwargs):

    tags = instance.tags.all()

    for tag in tags:
        # Compute the potential new difficulty for the TagProblem
        new_difficulty = instance.difficulty * tag.difficulty
        # Check if a TagProblem instance already exists for this tag and problem
        tag_problem_obj, created = TagProblem.objects.get_or_create(
            tag=tag,
            problem=instance.problem,
            defaults={'difficulty': new_difficulty}
        )
        # If the TagProblem instance exists but the new difficulty is greater than the current one, update it
        if not created and new_difficulty > tag_problem_obj.difficulty:
            tag_problem_obj.difficulty = new_difficulty
            tag_problem_obj.save()
