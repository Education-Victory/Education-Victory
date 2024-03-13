from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import UserAbilitySerializer
from question.models import Tag
from .models import UserAbility

User = get_user_model()

def home(request):
    # HTML for home page
    return render(request, 'common/home.html', {'root': settings.ROOT})

def practice(request):
    return render(request, 'common/practice.html', {'root': settings.ROOT})

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

def set_user_ability(user_id, ability_score=50):
    # Fetch the user by ID
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
        return

    all_tags = Tag.objects.all()

    for tag in all_tags:
        UserAbility.objects.update_or_create(
            user=user,
            tag=tag,
            defaults={'ability_score': ability_score}
        )


@receiver(post_save, sender=User)
def create_user_ability(sender, instance, created, **kwargs):
    if created:  # Check if a new instance was created
        set_user_ability(instance.id, default_ability_score)


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
