import urllib.parse
from datetime import timedelta
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from problem.models import Problem
from .models import CodingQuestion, ChoiceQuestion
from .serializers import CodingQuestionSerializer, ChoiceQuestionSerializer


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
