from django.shortcuts import render
from django.db.models import F
from requests import Response
from rest_framework import viewsets, status
from common.utils import cal_score
from .models import Question, Solution, Keypoint, Category
from .serializers import QuestionSerializer, SolutionSerializer, KeypointSerializer, CategorySerializer
from rest_framework.decorators import action
from common.models import UserSubmission
from common.utils import cal_score
from datetime import datetime, timedelta


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

        # Parse the user from request
        user = request.user
        if not user:
            # Handle unauthorized request here
            # TODO: Refactor the error message in serializer
            return Response("User not logged in",
                            status=status.HTTP_401_UNAUTHORIZED)

        # Get all submissions of current user
        submission = UserSubmission.objects.filter(user_id=user.id)

        # All solutions before filtering
        queryset = Solution.objects.all()
        group = self.request.query_params.get('group', None)
        count = self.request.query_params.get('count', 0)
        # Step 1: Implement filter
        if group is not None:
            queryset = queryset.filter(group=group)
        # TODO: define type enums as constants
        if type == 1:
            # queryset = queryset.filter(...)
            pass
        # Step 2: Calculate solution score
        res = []

        # Calculate the date num_days_ago days ago
        num_days_ago = 14
        user_freq_start_date = datetime.now().date() - timedelta(days=num_days_ago)
        # Count the number of user submissions within the last 14 days
        submission_count = submission.filter(
            created_at__gte=user_freq_start_date).count()
        submission_frequency = submission_count / num_days_ago
        is_review_mode = self.request.query_params.get('review', False)

        for this_solution in queryset:
            # Filter out user submissions for this particular solution
            this_submission_query = submission.filter(
                solution_id=this_solution.id).order_by('-created_at')
            # cal_score is a pure function have no database operation in it
            score = cal_score(
                user.ability, this_solution.ability, this_submission_query, metadata={
                    "submission_frequency": submission_frequency,
                    "is_review_mode": is_review_mode
                })
            # Add item for sorting
            res.append([score, this_solution])
        res.sort(reverse=True)
        # Retrieve back the solution obj
        res = [item[1] for item in res]
        serializer = SolutionSerializer(res[:count], many=True)
        return Response(serializer.data)


class KeypointViewSet(viewsets.ModelViewSet):
    serializer_class = KeypointSerializer

    def get_queryset(self):
        queryset = Keypoint.objects.all()
        return queryset
