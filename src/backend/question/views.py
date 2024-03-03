import urllib.parse
from datetime import timedelta
from django.db.models import Count, Q, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from problem.models import Problem
from .models import CodingQuestion, ChoiceQuestion, UserSubmission
from .serializers import CodingQuestionSerializer, ChoiceQuestionSerializer, UserSubmissionSerializer


LAST_YEAR = timezone.now() - timedelta(days=365)


class QuestionViewSet(viewsets.ViewSet):

    def list(self, request):
        problem_name = request.query_params.get('name')
        if not problem_name:
            return Response({"error": "Problem name is required"}, status=400)

        problem_name = problem_name.replace('-', ' ')
        try:
            problem = Problem.objects.get(name=problem_name)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found"}, status=404)

        response_data = {}

        if problem.category == 'system design':
            # For system design, all questions are ChoiceQuestion
            questions = ChoiceQuestion.objects.filter(problem=problem)
            response_data = {
                'understand': ChoiceQuestionSerializer(questions.filter(type='understand'), many=True).data,
                'analyze': ChoiceQuestionSerializer(questions.filter(type='analyze'), many=True).data,
                'implement': ChoiceQuestionSerializer(questions.filter(type='implement'), many=True).data,
            }
        elif problem.category == 'algorithm':
            # For algorithm, understand and analyze stages are ChoiceQuestion, implement stage is CodingQuestion
            choice_questions = ChoiceQuestion.objects.filter(problem=problem)
            coding_questions = CodingQuestion.objects.filter(problem=problem, type='implement')
            response_data = {
                'understand': ChoiceQuestionSerializer(choice_questions.filter(type='understand'), many=True).data,
                'analyze': ChoiceQuestionSerializer(choice_questions.filter(type='analyze'), many=True).data,
                'implement': CodingQuestionSerializer(coding_questions, many=True).data,
            }
        else:
            # Handle other categories if needed
            pass
        return Response(response_data)


class UserSubmissionViewSet(viewsets.ModelViewSet):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    @action(detail=False, methods=['post'], url_path='submit-answer')
    def submit_answer(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        question_type = data.get('question_type')
        question_id = data.get('question_id')
        correct = data.get('correct')
        content = data.get('content')

        # Determine the content_type based on the question_type
        if question_type == 'choice':
            content_type = ContentType.objects.get_for_model(ChoiceQuestion)
        elif question_type == 'coding':
            content_type = ContentType.objects.get_for_model(CodingQuestion)
        else:
            return Response({'error': 'Invalid question type'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the submission
        submission = UserSubmission.objects.create(
            user=user,
            content_type=content_type,
            object_id=question_id,
            correct=correct,
            content=content
        )

        return Response({'status': 'Answer submitted successfully'}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset().select_related('content_type').order_by('-created_at')
        problem_name = self.request.query_params.get('name', '').replace('-', ' ')
        question_type = self.request.query_params.get('type')

        if problem_name and question_type:
            try:
                problem = Problem.objects.get(name=problem_name)
            except Problem.DoesNotExist:
                return queryset.none()  # Problem not found, return an empty queryset

            # Determine the ContentType for ChoiceQuestion and CodingQuestion
            choice_content_type = ContentType.objects.get_for_model(ChoiceQuestion)
            coding_content_type = ContentType.objects.get_for_model(CodingQuestion)

            # Filter ChoiceQuestions and CodingQuestions based on problem and type
            choice_questions_ids = ChoiceQuestion.objects.filter(
                problem=problem, type=question_type).values_list('id', flat=True)
            coding_questions_ids = CodingQuestion.objects.filter(
                problem=problem, type=question_type).values_list('id', flat=True)

            # Filter submissions based on filtered questions and user
            filtered_submissions = queryset.filter(
                Q(content_type=choice_content_type, object_id__in=choice_questions_ids) |
                Q(content_type=coding_content_type, object_id__in=coding_questions_ids),
                user=self.request.user
            )

            # Now, we need to get the latest submission for each question
            latest_submissions = {}
            for submission in filtered_submissions:
                key = (submission.content_type_id, submission.object_id)
                if key not in latest_submissions:
                    latest_submissions[key] = submission

            # Convert the dictionary back to a QuerySet-like list for serialization
            latest_submissions_list = list(latest_submissions.values())

            # Depending on your DRF settings, you might need to manually serialize this list
            # because it's not a QuerySet. Use your serializer as usual.
            return latest_submissions_list
        else:
            return queryset.none()  # Return empty queryset if problem_name or question_type is not provided
