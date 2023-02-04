from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from.views import *


urlpatterns = [
    path('UserApi', UserListApiView.as_view()),
    path('UserScoreApi', UserScoreListApiView.as_view()),
    path('UserFavApi', UserFavListApiView.as_view()),
    path('UserFavApi/<int:pk>/', UserFavDetailApiView.as_view()),
    path('UserScoreApi/<int:pk>/', UserScoreDetailApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)