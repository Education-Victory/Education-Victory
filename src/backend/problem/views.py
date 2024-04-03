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
from .serializers import ProblemSerializer, CustomProblemSerializer
from question.models import Question, Tag, Milestone
from common.models import UserAbility


def problem(request, name):
    return render(request, 'problem/problem.html',
        {'root': settings.ROOT, 'name': name, 'user_id': request.user.id})


def get_tag_score(user, category, num=3):
    tags_in_tagproblem = TagProblem.objects.values_list('tag_id', flat=True).distinct()
    weak_tag_ability = UserAbility.objects.filter(
        user=user,
        tag__category=category,
        tag_id__in=Subquery(tags_in_tagproblem)
    ).select_related('tag').order_by('ability_score')[:num]

    return [
        {
            'tag_name': user_ability.tag.name,
            'tag_group': user_ability.tag.group,
            'tag_category': user_ability.tag.category,
            'ability_score': user_ability.ability_score
        }
        for user_ability in weak_tag_ability
    ]


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
        total_problems = 10
        difficulty_down = 10
        difficulty_up = 20
        problems = []
        if category == 'recommend':
            for cat, percentage in user_settings.items():
                num_problems = ceil(total_problems * (percentage / 100))
                tag_scores = get_tag_score(user, cat, num=3)
                collected_problems = 0
                for tag_info in tag_scores:
                    if collected_problems >= num_problems:
                        break
                    tag_name = tag_info['tag_name']
                    user_ability = tag_info['ability_score']
                    category_problems = Problem.objects.filter(
                        tags__name=tag_name,
                        category=cat,
                        tagproblem__difficulty__gte=user_ability - difficulty_down,
                        tagproblem__difficulty__lte=user_ability + difficulty_up
                    ).annotate(
                        difficulty=F('tagproblem__difficulty')
                    ).distinct().order_by('difficulty')[:num_problems - collected_problems]
                    for problem in category_problems:
                        tag_instance = Tag.objects.get(name=tag_name)
                        # Instead of fetching the tag instance separately, directly use tag_info
                        # And directly use the annotated difficulty
                        problems.append({
                            'problem': problem,
                            'tag': tag_instance,
                            'user_ability': user_ability,
                            'tag_difficulty': problem.difficulty  # Use the annotated difficulty
                        })
                    collected_problems += len(category_problems)
        else:
           tag_scores = get_tag_score(user, category, num=3)
           collected_problems = 0
           for tag_info in tag_scores:
                if collected_problems >= total_problems:
                    break
                tag_name = tag_info['tag_name']
                user_ability = tag_info['ability_score']
                category_problems = Problem.objects.filter(
                    tags__name=tag_name,
                    category=category,
                    tagproblem__difficulty__gte=user_ability - difficulty_down,
                    tagproblem__difficulty__lte=user_ability + difficulty_up
                ).annotate(
                    difficulty=F('tagproblem__difficulty')
                ).distinct().order_by('difficulty')[:total_problems - collected_problems]
                for problem in category_problems:
                    tag_instance = Tag.objects.get(name=tag_name)
                    problems.append({
                        'problem': problem,
                        'tag': tag_instance,
                        'user_ability': user_ability,
                        'tag_difficulty': problem.difficulty  # Use the annotated difficulty
                    })
                collected_problems += len(category_problems)
        serializer = CustomProblemSerializer(problems, many=True, context={'request': request})
        return Response({'problems': serializer.data})


def submission(request):
    pass
