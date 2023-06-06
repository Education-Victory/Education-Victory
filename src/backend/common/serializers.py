from rest_framework import serializers
from .models import UserSubmission

class UserSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubmission
        # Specifies the fields to be included in serialized representations of UserSubmission instances
        fields = ['id', 'user', 'solution', 'content', 'created_at', 'updated_at']
