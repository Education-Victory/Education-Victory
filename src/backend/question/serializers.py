from rest_framework import serializers
from .models import Question, Solution, Keypoint, UserKeypointScore, UserSubmission, Category

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = "__all__"
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question 
        fields = "__all__"
        
class KeypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keypoint
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserKeypointScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeypointScore
        fields = "__all__"
        
class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = "__all__"
    