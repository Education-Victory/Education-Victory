from django.urls import path, include

from.views import *


urlpatterns = [
    path('UserApi', UserListApiView.as_view()),
    path('UserScoreApi', UserScoreListApiView.as_view()),
    path('UserFavApi', UserFavListApiView.as_view()),
]