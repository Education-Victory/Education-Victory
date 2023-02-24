from rest_framework import serializers
from .models import UserSubmission

class UserSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubmission
        fields = ['id', 'user', 'solution', 'content', 'created_at', 'updated_at']
