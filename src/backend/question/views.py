import urllib.parse
from datetime import timedelta
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CodingQuestion, ChoiceQuestion
from .serializers import CodingQuestionSerializer, CodingQuestionBasicSerializer, ChoiceQuestionSerializer


LAST_YEAR = timezone.now() - timedelta(days=365)


class CodingQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = CodingQuestionBasicSerializer

    def get_queryset(self):
        queryset = CodingQuestion.objects.all()
        category = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)
        if category:
            queryset = queryset.filter(category=category)
        if name:
            queryset = queryset.filter(name=name)
        return queryset


@api_view(['GET'])
def get_recommend_task(request):
    '''
    User can get today tasks info in practice page
    '''
    state = request.GET.get('state', 'new')
    count = int(request.GET.get('count', 1))
    task = get_today_task(request.user, state, count)
    res = TaskSerializer(task, many=True)
    return Response(res.data)


@api_view(['POST'])
def generate_daily_task(request):
    '''
    Generate daily task
    '''
    try:
        generate_task_from_user(request.user)
    except:
        return Response({'error': 'Can\'t not generate task'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_task(request):
    pass


@api_view(['GET'])
def get_question_lst(request):
    '''
    Get question list based on query
    '''
    topic = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')
    category = urllib.parse.unquote(request.GET.get('category'))
    company = request.GET.get('company')
    progress = request.GET.get('progress', None)
    frequency = request.GET.get('frequency', None)
    return get_question_from_queryset(topic, difficulty, category, company, progress, frequency)

def get_question_from_queryset(topic, difficulty, category, company, progress, frequency):
    if topic == 'Algorithm':
        queryset_one = get_algorithm_queryset('coding', difficulty, category, company)
        queryset_two = get_algorithm_queryset('choice', difficulty, category, company)
        serializer_one = CodingQuestionSerializer(queryset_one, many=True)
        serializer_two = ChoiceQuestionSerializer(queryset_two, many=True)
        merged_data = list(serializer_one.data) + list(serializer_two.data)
    if progress == 'ascending':
        return Response(sorted(merged_data, key=lambda x: x['progress']))
    elif progress == 'descending':
        return Response(sorted(merged_data, key=lambda x: x['progress'], reverse=True))
    if frequency == 'ascending':
        return Response(sorted(merged_data, key=lambda x: x['frequency']))
    elif frequency == 'descending':
        return Response(sorted(merged_data, key=lambda x: x['frequency'], reverse=True))
    return Response(merged_data)

def get_algorithm_queryset(model, difficulty, category, company):
    if model == 'coding':
        queryset = CodingQuestion.objects.all()
    elif model == 'choice':
        queryset = ChoiceQuestion.objects.all()
    if difficulty and difficulty != 'All':
        diffculty_range = {
            'Beginner': (1, 200),
            'Easy': (201, 400),
            'Medium': (401, 600),
            'Hard': (601, 800),
            'Expert': (801, 1000)
            }
        queryset = queryset.filter(diffculty__range=diffculty_range[difficulty])
    # Filter based on category
    if category and category != 'All':
        queryset = queryset.filter(category=category)
    last_year_conditions = Q(problem__frequency_problem__created_at__gte=LAST_YEAR)
    total_conditions = Q()
    if company and company != 'All':
        last_year_conditions &= Q(problem__frequency_problem__company=company)
        total_conditions &= Q(problem__frequency_problem__company=company)
        queryset = queryset.annotate(
            frequency=Count(
                'problem__frequency_problem',
                filter=last_year_conditions
            ),
            total_frequency=Count(
                'problem__frequency_problem',
                filter=total_conditions
            )
        )
        queryset = queryset.filter(frequency__gt=0)
    else:
        queryset = queryset.annotate(
            frequency=Count(
                'problem__frequency_problem',
                filter=last_year_conditions
            ),
            total_frequency=Count(
                'problem__frequency_problem',
                filter=total_conditions
            )
        )
    return queryset
