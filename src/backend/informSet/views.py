from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions, status
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# User Views
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = WebUser.objects.all()
    serializer_class = UserSerializer


class UserScoreViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]                        
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer
    def get(self, request, *args, **kwargs):
        queryset = UserScore.objects.filter(user_id = request.user.id)
        serializer = UserFavSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserScoreModifyApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_score_object(self, id: int, scoreCategory: int):
        userscore = UserScore.objects.get(score_category = scoreCategory, user_id = id)
        return userscore

    def get(self, request, *args, **kwargs):
        '''
        get category scores by category names
        '''
        userscore = self.get_score_object(request.user.id, kwargs["score_category"])
        if not userscore:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = UserScoreSerializer(userscore)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        userscore = self.get_score_object(request.user.id, kwargs["score_category"])
        if not userscore:
            return Response(status = status.HTTP_404_NOT_FOUND)
        scoreCategory = ""
        score = ""
        # get the request data(if they exist)
        scoreCategory = userscore.score_category
        if request.data.get('score'):
            score = request.data.get('score')
        else:
            score = userscore.score

        # wrap up data in the json         
        data = {
            #'id' : userscore.id,
            'user_id': request.user.id,
            'score_category': scoreCategory,
            'score': score
        }
        serializer = UserScoreSerializer(userscore, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#UserFav views
class UserFavViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()
    def get(self, request, *args, **kwargs):
        queryset = UserFav.objects.filter(user_id = request.user.id)
        serializer = UserFavSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# list the userfav in different pages
class UserFavShowPage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        page = kwargs["page"]
        pageSize = kwargs["pageSize"]
        queryset = UserFav.objects.all()
        paginator = Paginator(queryset, pageSize)
        try:
            user_fav = paginator.page(page)
        except PageNotAnInteger:
            user_fav = paginator.page(1)
        except EmptyPage:
            user_fav = paginator.page(paginator.num_pages)
        serializer = UserFavSerializer(user_fav, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
