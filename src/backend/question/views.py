from django.shortcuts import render
from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer

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
