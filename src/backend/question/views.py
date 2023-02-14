from django.shortcuts import render
from rest_framework import viewsets
from .models import Question, Solution, Keypoint
from .serializers import QuestionSerializer, SolutionSerializer, KeypointSerializer

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
