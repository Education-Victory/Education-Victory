from django.shortcuts import render
from django.db.models import F
from rest_framework import viewsets
from common.utils import cal_score
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

    @action(detail=True, methods=['get'])
    def recommend_solutions(self, request):
        # We can call this API like
        # /api/question/recommend_solutions?type=1&group=2&count=3
        #
        # user: request user
        # type: 1. review_mode 2. submit more than 3 times
        # group: Data structures / Algorithms / Technique / Others
        # count: total count of solution should return
        user = request.user
        submission = UserSubmission.objects.filter(...)
        group = self.request.query_params.get('group', None)
        count = self.request.query_params.get('count', 0)
        # Step 1: Implement filter
        if group is not None:
            queryset = queryset.filter(...)
        if type == 1:
            queryset = queryset.filter(...)
        # Step 2: Calculate solution score
        res = []
        for query in queryset:
            # cal_score is a pure function have no database operation in it
            score = utils.cal_score(user.ability, query.ability, submission...)
            res.append(score)
        res.sort(reverse=True)
        serializer = SolutionSerializer(res[:count], many=True)
        return Response(serializer.data)


class KeypointViewSet(viewsets.ModelViewSet):
    serializer_class = KeypointSerializer

    def get_queryset(self):
        queryset = Keypoint.objects.all()
        return queryset
