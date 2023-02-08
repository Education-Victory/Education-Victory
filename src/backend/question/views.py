from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question, Solution, Keypoint, UserKeypointScore, UserSubmission
from .serializers import QuestionSerializer, SolutionSerializer, KeypointSerializer, UserKeypointScoreSerializer, UserSubmissionSerializer

class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()  

    def get_queryset(self):
        # support
        # 1. getting all questions 
        # 2. query questions starts with certain string
        queryset = Question.objects.all()  
        name_starts_wtih = self.request.query_params.get('name_starts_wtih', None)
        if name_starts_wtih is not None:
            queryset = queryset.filter(name__startswith=name_starts_wtih)
        return queryset

class KeypointList(APIView):    
    def get_keypoint_ids(self, request):
        # request should include solution id in order to query all keypoints related to this solution
        solution = Solution.objects.get(id=request.solution_id)
        lst_keypoints_ids = solution.keypoints
        return lst_keypoints_ids 
    

    def get(self, request, format=None):
        # 1. get a list of keypoints 
        lst_keypoints_ids = self.get_keypoint_ids(request)
        keypoint_objs = Keypoint.objects.filter(pk__in=lst_keypoints_ids)
        serializer = KeypointSerializer(keypoint_objs)
        return Response(serializer.data)