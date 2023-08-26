from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.models import Task
from .models import Solution, Category, CodingQuestion, ChoiceQuestion
from .serializers import SolutionSerializer, CategorySerializer, BasicTaskSerializer, TaskSerializer
from .utils.task import get_task

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class SolutionViewSet(viewsets.ModelViewSet):
    serializer_class = SolutionSerializer

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

    coding_question = get_question_from_query(CodingQuestion, category, question_type, difficulty)
    choice_question = get_question_from_query(CodingQuestion, category, question_type, difficulty)

def get_question_from_query(model, category, question_type, difficulty):
    queryset = model.objects.all()
    queryset.filter(category=category)
