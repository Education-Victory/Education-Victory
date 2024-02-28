from django.conf import settings
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Problem
from .serializers import ProblemSerializer

class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        queryset = Problem.objects.all()
        name = self.request.query_params.get('name', None)
        print(name)
        if name is not None:
            name = name.replace('-', ' ')
            queryset = queryset.filter(name=name)
        return queryset


def problem(request, name):
    return render(request, 'problem/problem.html',
        {'root': settings.ROOT, 'name': name, 'user_id': request.user.id})
