from django.shortcuts import render
from django.db.models import F
from rest_framework import viewsets
from datetime import datetime, timedelta
from django.core.paginator import Paginator


from common.models import User, UserSubmission
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
        # Filters questions by category if provided in the query parameters
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class SolutionViewSet(viewsets.ModelViewSet):
    serializer_class = SolutionSerializer

    def __get_query_set_helper(self):
        queryset = Solution.objects.all()
        # Filters Solution by category, category_name, question_name and keypoint if provided in the query parameters
        category = self.request.query_params.get('category', None)
        category_name = self.request.query_params.get('category_name', None)
        question_name = self.request.query_params.get('question_name', None)
        keypoint = self.request.query_params.get('keypoint', None)
        solution_type = self.request.query_params.get('type', None)
        if category_name is not None:
            queryset = queryset.filter(category__name=category_name)
        if question_name is not None:
            queryset = queryset.filter(question__name=question_name)
        if category is not None:
            queryset = queryset.filter(category=category)
        if keypoint is not None:
            queryset = queryset.filter(keypoint=keypoint)
        if solution_type is not None and solution_type != 'all':
            queryset = queryset.filter(type=solution_type)
        return queryset

    def get_queryset(self):
        query_set = self.__get_query_set_helper()
        limit = self.request.query_params.get('limit', 10)
        page = self.request.query_params.get('page', 1)
        paginator = Paginator(query_set, limit)
        return paginator.get_page(page)

    def get_queryset_by_suggested_level(self, userId, is_review_mode=False):
        userObj = User.objects.get(id=userId)

        date_range = 14
        today = datetime.now().date()
        elapsed_date = today - timedelta(days=date_range)

        userFrequency = (UserSubmission.objects.filter(
            created_at__gte=elapsed_date, created_at__lte=today).count()) / date_range

        solution_query_set = self.__get_query_set_helper(self)
        for solutionObj in solution_query_set:
            suggestion_level = SolutionSerializer.get_suggestion_level(solutionObj=solutionObj, userObj=userObj, paramObj={
                "w1": 1, "w2": 1, "w3": 1, "w4": 1,
                "is_review_mode": is_review_mode,
                "user_frequency": userFrequency
            })
            solutionObj.suggestion_level = suggestion_level
        solution_query_set.order_by('-suggestion_level')

        # Pagination
        limit = self.request.query_params.get('limit', 10)
        page = self.request.query_params.get('page', 1)
        paginator = Paginator(solution_query_set, limit)
        return paginator.get_page(page)


class KeypointViewSet(viewsets.ModelViewSet):
    serializer_class = KeypointSerializer

    def get_queryset(self):
        queryset = Keypoint.objects.all()
        return queryset
