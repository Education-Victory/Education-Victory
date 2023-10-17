from datetime import timedelta
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.models import Task
from .models import Category, CodingQuestion, ChoiceQuestion, ProblemFrequency
from .serializers import CategorySerializer, \
        TaskSerializer, CodingQuestionSerializer, ChoiceQuestionSerializer
from .utils.task import get_task, get_today_task, generate_task_from_user


LAST_YEAR = timezone.now() - timedelta(days=365)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        state = self.request.query_params.get('state', None)
        count = int(self.request.query_params.get('count', '1'))
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
    difficulty = request.GET.get('difficulty', None)
    category = request.GET.get('cateogry', None)
    company = request.GET.get('company', None)
    progress = request.GET.get('progress', None)
    frequency = request.GET.get('frequency', None)
    return get_question_from_queryset(difficulty, category, company, progress, frequency)

def get_question_from_queryset(difficulty, category, company, progress, frequency):
    queryset_one = get_queryset_from_model('coding', difficulty, category, company)
    queryset_two = get_queryset_from_model('choice', difficulty, category, company)
    serializer_one = CodingQuestionSerializer(queryset_one, many=True)
    serializer_two = ChoiceQuestionSerializer(queryset_two, many=True)
    merged_data = list(serializer_one.data) + list(serializer_two.data)

    if progress:
        if progress == 'ascending':
            return Response(sorted(merged_data, key=lambda x: x['progress']))
        else:
            return Response(sorted(merged_data, key=lambda x: x['progress'], reverse=True))
    if frequency:
        if frequency == 'ascending':
            return Response(sorted(merged_data, key=lambda x: x['frequency']))
        else:
            return Response(sorted(merged_data, key=lambda x: x['frequency'], reverse=True))
    return Response(merged_data)


def get_queryset_from_model(model, difficulty, category, company):
    # Get basic Queryset by model
    if model == 'coding':
        queryset = CodingQuestion.objects.all()
        qtype = 'coding'
    elif model == 'choice':
        queryset = ChoiceQuestion.objects.all()
        qtype = 'choice'
    # Filter based on difficulty
    if difficulty:
        diffculty_range = {
            'Beginner': (1, 200),
            'Easy': (201, 400),
            'Medium': (401, 600),
            'Hard': (601, 800),
            'Expert': (801, 1000)
            }
        queryset = queryset.filter(diffculty__range=diffculty_range[difficulty])
    # Filter based on category
    if category:
        queryset = queryset.filter(category=category)
    # Filter based on company
    if company:
        queryset = queryset.filter(company=company)
        # Count the frequency based on company
        problem_frequency = ProblemFrequency.objects.filter(
            question_id=OuterRef('id'), company=company, qtype=qtype, created_at__gte=LAST_YEAR).values(
            "question_id").annotate(count=Count("id")).values("count")
        queryset = queryset.annotate(frequency=Subquery(problem_frequency))
    else:
        problem_frequency = ProblemFrequency.objects.filter(
            question_id=OuterRef('id'), qtype=qtype, created_at__gte=LAST_YEAR).values(
            "question_id").annotate(count=Count("id")).values("count")
        queryset = queryset.annotate(frequency=Subquery(problem_frequency))
    return queryset
