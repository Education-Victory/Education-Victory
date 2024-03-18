from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.viewsets import ModelViewSet
from .models import Problem
from .serializers import ProblemSerializer
from question.models import Question

class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        queryset = Problem.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            name = name.replace('-', ' ')
            queryset = queryset.filter(name=name)
        return queryset


def problem(request, name):
    return render(request, 'problem/problem.html',
        {'root': settings.ROOT, 'name': name, 'user_id': request.user.id})


def get_weak_tag(user, category, num=3):
    weak_tag_ability = UserAbility.objects.filter(
        user=user,
        tag__category=category
    ).order_by('ability_score')[:num]

    return weak_tag_ability

def recommend_problem(request):
    user = request.user  # Assuming you have user authentication set up
    category = request.GET.get('category', 'recommend')
    # Assuming user.settings is a dict with categories as keys and percentage as values
    user_settings = getattr(user, 'settings', {'algorithm': 100})  # Default to 100% algorithm for demonstration
    # If category is 'recommend', determine category based on user settings (simplified logic)
    if category == 'recommend':
        # Simplified: just pick the first category for demonstration
        category = list(user_settings.keys())[0]
        weak_tag = get_weak_tag(user, category)
    else:

        weak_tag = get_weak_tag(user, category)

        problems = Problem.objects.filter(
            tagproblem__tag=weakest_tag,
            category=category
        ).distinct()[:5]

    # Convert problems to JSON
    problems_json = [{'id': problem.id, 'name': problem.name, 'category': problem.category} for problem in problems]
    return JsonResponse({'problems': problems_json})


@receiver(post_save, sender=Question)
def update_tag_problem(sender, instance, **kwargs):
    instance.update_tag_problem()
