from math import ceil
from collections import defaultdict
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import ExpressionWrapper, F, Q, IntegerField, DurationField, Sum, Case, When, Subquery, Count, Avg
from django.db.models.functions import Now, ExtractDay
from django.dispatch import receiver
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Problem, ProblemFrequency, TagProblem
from .serializers import ProblemSerializer, ProblemFrequencySerializer, CustomProblemSerializer
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
        queryset = super().get_queryset()  # Get the initial queryset
        problem_name = self.request.query_params.get('name')

        if problem_name:
            # Replace hyphens with spaces to match the original format
            formatted_name = problem_name.replace('-', ' ')
            # Filter the queryset based on the exact match of the name
            queryset = queryset.filter(name=formatted_name)

        return queryset


class ProblemFrequencyViewSet(ModelViewSet):
    queryset = ProblemFrequency.objects.all().select_related('problem').prefetch_related('problem__tags')
    serializer_class = ProblemFrequencySerializer

    def annotate_scores(self, instance):
        now = timezone.now()
        days_since_created = (now - instance.created_at).days  # Calculate the number of days since creation

        # Calculate the score using the extracted days
        score = int(100 / (1 + days_since_created / 60))
        return score

    def get_queryset(self):
        queryset = super().get_queryset()
        company = self.request.query_params.get('company')
        frequency = self.request.query_params.get('frequency')
        category = self.request.query_params.get('category')
        stage = self.request.query_params.get('stage')
        position_type = self.request.query_params.get('position_type')

        # Filter based on query parameters
        if company and company != 'All':
            queryset = queryset.filter(company=company)
        if category and category != 'All':
            queryset = queryset.filter(problem__category=category)
        if stage and stage != 'All':
            queryset = queryset.filter(stage=stage)
        if position_type and position_type != 'All':
            queryset = queryset.filter(position_type=position_type)

        queryset = queryset.annotate(
            difficulty=Avg('problem__tags__difficulty')
        )
        scores = defaultdict(int)
        exist_queryset = dict()
        # Iterate over the filtered queryset
        annotated_queryset = []
        for instance in queryset:
            score = self.annotate_scores(instance)
            if instance.problem.id not in exist_queryset:
                exist_queryset[instance.problem.id] = instance
                annotated_queryset.append(instance)
                instance.total_score = score
            else:
                exist_queryset[instance.problem.id].total_score += score
        return annotated_queryset

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
