from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import WebUser
from .serializers import WebUserSerializer

class WebUserListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Webuser items for given requested user
        '''
        webUser = WebUser.objects.filter(user = request.user.id)
        serializer = WebUserSerializer(webUser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the webuser with given todo data
        '''
        data = {
            'user': request.user.id,
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'avatar': request.data.get('avatar')
        }
        serializer = WebUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #3. PUT
            
    def put(self, request, *args, **kwargs):
        '''
        Create the webuser with given todo data
        '''
        webUser = WebUser.objects.get(user = request.user.id)
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'avatar': request.data.get('avatar')
        }
        serializer = WebUserSerializer(webUser, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    