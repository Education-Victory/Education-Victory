from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.models import Task
from .models import Solution, Category, CodingQuestion, ChoiceQuestion
from .serializers import SolutionSerializer, CategorySerializer, \
        TaskSerializer, CodingQuestionSerializer, ChoiceQuestionSerializer
from .utils.task import get_task, get_today_task, generate_daily_task_for_user


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
    Every day we will create tasks for user,
    '''
    if request.user.is_superuser:
        generate_daily_task_for_user()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_single_test(request):
    pass


@api_view(['GET'])
def get_question_lst(request):
    '''
    Get question list based on query
    '''

    category = request.GET.get('cateogry', None)
    question_type = request.GET.get('type', None)
    difficulty = request.GET.get('difficulty', None)
    progress = request.GET.get('progress', 'ascending')
    frequency = request.GET.get('frequency', 'ascending')
    return get_question_from_query(
        category, question_type, difficulty, progress, frequency)


def get_question_from_query(category, question_type, difficulty, progress, frequency):
    # TODO: Add progress and frequency
    if question_type == 'All':
        queryset_one = get_queryset_from_model(CodingQuestion, category, difficulty)
        queryset_two = get_queryset_from_model(ChoiceQuestion, category, difficulty)
        serializer_one = CodingQuestionSerializer(queryset_one, many=True)
        serializer_two = ChoiceQuestionSerializer(queryset_two, many=True)
        merged_data = list(serializer_one.data) + list(serializer_two.data)
        return Response(merged_data)
    else:
        if question_type == 'Coding':
            queryset = get_queryset_from_model(CodingQuestion, category, difficulty)
            serializer = CodingQuestionSerializer(queryset, many=True)
            return Response(serializer.data)
        elif question_type == 'Choice':
            queryset = get_queryset_from_model(ChoiceQuestion, category, difficulty)
            serializer = ChoiceQuestionSerializer(queryset, many=True)
            return Response(serializer.data)


def get_queryset_from_model(model, category, difficulty):
    queryset = model.objects.all()
    if category:
        queryset.filter(solution__category_id=category)
    if difficulty:
        diffculty_range = {
            'Level One': (1, 20),
            'Level Two': (21, 40),
            'Level Three': (41, 60),
            'Level Four': (61, 80),
            'Level Five': (81, 100)
            }
        queryset = model.objects.filter(diffculty__range=diffculty_range[difficulty])
    return queryset

