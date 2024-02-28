from rest_framework.viewsets import ModelViewSet
from .models import Problem
from .serializers import ProblemSerializer

class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
