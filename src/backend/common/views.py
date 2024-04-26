from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserAbilitySerializer, UserActivitySerializer, UserSubmissionSerializer, ReviewSerializer
from question.models import Question, Tag, Milestone, QuestionMilestone
from .models import UserAbility, UserActivity, UserSubmission
from .utils import evaluate_submission


User = get_user_model()

def home(request):
    # HTML for home page
    return render(request, 'common/home.html', {'root': settings.ROOT})

def practice(request):
    return render(request, 'common/practice.html', {'root': settings.ROOT})

def roadmap(request):
    return render(request, 'common/roadmap.html', {'root': settings.ROOT})

def evaluation(request, type):
    if type == 'coding':
        return render(request, 'common/evaluation/coding.html')

def evaluation_simple(request):
    # Use three simple questions for simple evaluation to determine which level the user belongs to
    question_lst = {
        'data': [
        {
            'title': 'How many years of programming experience do you have?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 1 years',
                    'value': 0
                },
                {
                    'text': '1 - 3 years',
                    'value': 20
                },
                {
                    'text': '3 - 6 years',
                    'value': 30
                },
                {
                    'text': '> 6 years',
                    'value': 40
                },
            ]
        },
        {
            'title': 'How many algorithm problems have you solved?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 50',
                    'value': 0
                },
                {
                    'text': '50 - 100',
                    'value': 20
                },
                {
                    'text': '100 - 300',
                    'value': 30
                },
                {
                    'text': '> 300',
                    'value': 40
                },
            ]
        },
        {
            'title': 'When do you expect to begin the interview?',
            'description': '',
            'type': 'single',
            'choice': [
                {
                    'text': '< 2 weeks',
                    'value': 0
                },
                {
                    'text': '2 weeks - 1 month',
                    'value': 20
                },
                {
                    'text': '1 month - 3 months',
                    'value': 30
                },
                {
                    'text': '> 3 months',
                    'value': 40
                },
            ]
        }]
    }
    return JsonResponse(question_lst)

def set_user_ability(user_id, default_ability=None):
    if not default_ability:
        default_ability = {
            'algorithm': 30, 'system-design': 20, 'computer-science': 30,
            'behavioral': 30, 'resume': 30
        }

    all_tags = Tag.objects.all()
    user = User.objects.get(pk=user_id)

    for tag in all_tags:
        # Get the default level for the tag's category, fall back to a default value if the category isn't in the dict
        user_level = default_ability.get(tag.category, 20)  # 20 is a fallback default value

        ability_score = max(0, user_level - (tag.difficulty - 20) // 3)
        UserAbility.objects.update_or_create(
            user=user,
            tag=tag,
            defaults={'ability_score': ability_score}
        )


@receiver(post_save, sender=User)
def create_user_ability(sender, instance, created, **kwargs):
    if created:  # Check if a new instance was created
        set_user_ability(instance.id)


class UserAbilityViewSet(viewsets.ModelViewSet):
    serializer_class = UserAbilitySerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag__category']

    def get_queryset(self):
        user = self.request.user
        tag_category = self.request.query_params.get('tag_category', None)
        queryset = UserAbility.objects.filter(user=user)
        if tag_category:
            queryset = queryset.filter(tag__category=tag_category)
        return queryset


class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer


class UserSubmissionViewSet(viewsets.ModelViewSet):
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():  # Ensure data integrity with transaction
            response = super().create(request, *args, **kwargs)

            if response.status_code == status.HTTP_201_CREATED:
                submission_data = response.data
                if submission_data.get('g_type') == 0:
                    # Extract necessary data from the submission
                    user = request.user
                    problem_id = submission_data.get('problem_id')
                    question_id = submission_data.get('question_id')

                    # Step 1: Find all questions related to the problem
                    related_questions = Question.objects.filter(problem_id=problem_id)

                    # Step 2: Collect all unique milestones for those questions
                    # Note: This uses a set to avoid duplicate milestones
                    milestones = set()
                    for question in related_questions:
                        for milestone in question.milestone.all():
                            milestones.add(milestone)

                    # Step 3: Update or create QuestionMilestone for each milestone
                    for milestone in milestones:
                        QuestionMilestone.objects.update_or_create(
                            user=user,
                            question_id=question_id,  # Assuming you want to link to the current question
                            milestone=milestone,
                            defaults={'state': True}
                        )

            return response



class ReviewAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            qu = Question.objects.get(pk=data['question_id'])
            # Evaluate based on question desc, answer, explain and user submission
            grade, tip = evaluate_submission(qu.desc['desc'], qu.desc['answer'], qu.desc['explain'], data['content'])
            return Response({
                'grade': grade,
                'tip': tip,
            })
        else:
            return Response(serializer.errors, status=400)
