from django.shortcuts import render
from rest_framework import viewsets
from .models import UserSubmission
from .serializers import UserSubmissionSerializer

class UserSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubmissionSerializer

    def get_queryset(self):
        queryset = UserSubmission.objects.all()
        return queryset
