from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import UserAbilitySerializer, UserActivitySerializer
from question.models import Tag
from .models import UserAbility, UserActivity

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

def set_user_ability(user_id, default_ability=None):
    if not default_ability:
        default_ability = {
            'algorithm': 30, 'system-design': 30, 'computer-science': 30,
            'behavioral': 30, 'resume': 30
        }

    all_tags = Tag.objects.all()
    user = User.objects.get(pk=user_id)

    for tag in all_tags:
        # Get the default level for the tag's category, fall back to a default value if the category isn't in the dict
        user_level = default_ability.get(tag.category, 20)  # 20 is a fallback default value

        ability_score = user_level - (tag.difficulty - 20) // 3
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
