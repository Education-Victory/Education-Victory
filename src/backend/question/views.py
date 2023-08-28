from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.models import Task
from .models import Solution, Category, CodingQuestion, ChoiceQuestion
from .serializers import SolutionSerializer, CategorySerializer, BasicTaskSerializer, TaskSerializer,  \
        CodingQuestionSerializer, ChoiceQuestionSerializer
from .utils.task import get_task

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Solution.objects.all()
        # Filters Solution by category, category_name, question_name and keypoint if provided in the query parameters
        category = self.request.query_params.get('category', None)
        category_name = self.request.query_params.get('category_name', None)
        question_name = self.request.query_params.get('question_name', None)
        keypoint = self.request.query_params.get('keypoint', None)
        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)
        if question_name is not None:
            queryset = queryset.filter(question__name=question_name)
        if category is not None:
            queryset = queryset.filter(category=category)
        if keypoint is not None:
            queryset = queryset.filter(keypoint=keypoint)
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        state = self.request.query_params.get('state', None)
        count = self.request.query_params.get('count', None)
        return get_recommend_task(state, count)


@api_view(['GET'])
def get_recommend_task(request):
    '''
    Get basic task info
    '''
    state = request.GET.get('state', 'new')
    count = int(request.GET.get('count', 1))
    task = get_task(request.user.id, state, count)
    res = BasicTaskSerializer(task, many=True)
    return Response(res.data)


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
        queryset.filter(solution_id__category_id=category)
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

