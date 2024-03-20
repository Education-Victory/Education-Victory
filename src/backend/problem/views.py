from math import ceil
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F, Q, Subquery
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Problem, TagProblem
from .serializers import ProblemSerializer
from question.models import Question
from common.models import UserAbility


def problem(request, name):
    return render(request, 'problem/problem.html',
        {'root': settings.ROOT, 'name': name, 'user_id': request.user.id})


def get_weak_tag(user, category, num=3):
    # First, get a queryset of tag IDs that exist in TagProblem.
    tags_in_tagproblem = TagProblem.objects.values_list('tag_id', flat=True).distinct()

    # Now, filter UserAbility objects for the given user and category,
    # ensuring that the tag is one of those present in TagProblem.
    weak_tag_ability = UserAbility.objects.filter(
        user=user,
        tag__category=category,
        tag_id__in=Subquery(tags_in_tagproblem)
    ).order_by('ability_score')[:num]

    return [user_ability.tag for user_ability in weak_tag_ability]


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
        user_settings = user_info.get('settings', {'algorithm': 50, 'system-design': 30, 'behavioral': 20})
        total_problems = 10  # Total number of problems to return
        # Define a margin or threshold for difficulty above the user's ability
        difficulty_down = 10
        difficulty_up = 20
        problems = []
        if category == 'recommend':
            for cat, percentage in user_settings.items():
                num_problems = ceil(total_problems * (percentage / 100))
                weak_tags = get_weak_tag(user, cat, num=3)  # Fetch more tags to have options
                collected_problems = 0

                for tag in weak_tags:
                    if collected_problems >= num_problems:
                        break  # Stop if we have collected enough problems
                    user_ability = UserAbility.objects.get(user=user, tag=tag).ability_score
                    category_problems = Problem.objects.filter(
                        tags=tag,  # Filter by current tag
                        category=cat,
                        tagproblem__difficulty__gte=user_ability - difficulty_down,
                        tagproblem__difficulty__lte=user_ability + difficulty_margin
                    ).annotate(
                        difficulty=F('tagproblem__difficulty')
                    ).order_by('difficulty')[:num_problems - collected_problems]
                    problems.extend(list(category_problems))
                    collected_problems += len(category_problems)
        else:
            weak_tags = get_weak_tag(user, category, num=3)  # Fetch more tags
            collected_problems = 0
            for tag in weak_tags:
                if collected_problems >= total_problems:
                    break
                user_ability = UserAbility.objects.get(user=user, tag=tag).ability_score

                category_problems = Problem.objects.filter(
                    tags=tag,
                    category=category,
                    tagproblem__difficulty__gte=user_ability - difficulty_down,
                    tagproblem__difficulty__lte=user_ability + difficulty_margin
                ).annotate(
                    difficulty=F('tagproblem__difficulty')
                ).order_by('difficulty')[:total_problems - collected_problems]

                problems.extend(list(category_problems))
                collected_problems += len(category_problems)

        serializer = ProblemSerializer(problems, many=True)
        return Response({'problems': serializer.data})
