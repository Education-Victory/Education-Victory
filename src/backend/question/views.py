from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.models import Task
from .models import Solution, Category, CodingQuestion, ChoiceQuestion
from .serializers import SolutionSerializer, CategorySerializer, \
        TaskSerializer, CodingQuestionSerializer, ChoiceQuestionSerializer
from .utils.task import get_task, get_today_task, generate_task_from_user


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
    category = request.GET.get('cateogry', None)
    difficulty = request.GET.get('difficulty', None)
    progress = request.GET.get('progress', 'ascending')
    frequency = request.GET.get('frequency', 'ascending')
    return get_question_from_query(category, difficulty, progress, frequency)

def get_question_from_query(category, difficulty, progress, frequency):
    queryset_one = get_queryset_from_model(CodingQuestion, category, difficulty)
    queryset_two = get_queryset_from_model(ChoiceQuestion, category, difficulty)
    serializer_one = CodingQuestionSerializer(queryset_one, many=True)
    serializer_two = ChoiceQuestionSerializer(queryset_two, many=True)
    merged_data = list(serializer_one.data) + list(serializer_two.data)
    return Response(merged_data)

def get_queryset_from_model(model, category, difficulty):
    queryset = model.objects.all()
    if category:
        queryset.filter(solution__category_id=category)
    if difficulty:
        diffculty_range = {
            'Beginner': (1, 200),
            'Easy': (201, 400),
            'Medium': (401, 600),
            'Hard': (601, 800),
            'Expert': (801, 1000)
            }
        queryset = model.objects.filter(diffculty__range=diffculty_range[difficulty])
    return queryset
