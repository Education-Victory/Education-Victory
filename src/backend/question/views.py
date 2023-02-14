from django.shortcuts import render
from rest_framework import viewsets
from .models import Question, Solution, Keypoint, Category
from .serializers import QuestionSerializer, SolutionSerializer, KeypointSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        category = self.request.query_params.get('category', None)
        sub_category = self.request.query_params.get('sub_category', None)
        if category is not None:
            queryset = queryset.filter(category__category_name=category)
        if sub_category is not None:
            queryset = queryset.filter(category__id=sub_category)
        return queryset

class SolutionViewSet(viewsets.ModelViewSet):
    serializer_class = SolutionSerializer

    def get_queryset(self):
        queryset = Solution.objects.all()
        return queryset

class KeypointViewSet(viewsets.ModelViewSet):
    serializer_class = KeypointSerializer

    def get_queryset(self):
        queryset = Keypoint.objects.all()
        return queryset
