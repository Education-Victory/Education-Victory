from math import ceil
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Problem
from .serializers import ProblemSerializer
from question.models import Question


def problem(request, name):
    return render(request, 'problem/problem.html',
        {'root': settings.ROOT, 'name': name, 'user_id': request.user.id})


def get_weak_tag(user, category, num=3):
    weak_tag_ability = UserAbility.objects.filter(
        user=user,
        tag__category=category
    ).order_by('ability_score')[:num]

    return weak_tag_ability


class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        queryset = Problem.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            name = name.replace('-', ' ')
            queryset = queryset.filter(name=name)
        return queryset


class RecommendProblemView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        category = request.query_params.get('category', 'recommend')
        user_info = getattr(user, 'info', {})
        user_settings = user_info.get('settings', {'algorithm': 50, 'system_design': 30, 'behavioral': 20})
        total_problems = 6  # Total number of problems to return

        problems = []

        if category == 'recommend':
            # Calculate the number of problems to fetch for each category based on the percentages
            for cat, percentage in user_settings.items():
                num_problems = ceil(total_problems * (percentage / 100))
                weak_tag = get_weak_tag(user, cat, num=1)
                # Fetch problems for each category based on the weak tag and the calculated number
                category_problems = Problem.objects.filter(
                    tagproblem__tag=weak_tag,
                    category=cat
                ).annotate(
                    difficulty=F('tagproblem__difficulty')
                ).order_by('-difficulty')[:num_problems]
                problems.extend(list(category_problems))
        else:
            # Fetch problems for the explicitly requested category
            problems = Problem.objects.filter(
                category=category
            ).annotate(
                difficulty=F('tagproblem__difficulty')
            ).order_by('-difficulty')[:total_problems]

        # Serialize the problem instances
        serializer = ProblemSerializer(problems, many=True)
        return Response({'problems': serializer.data})
