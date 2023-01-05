from django.urls import path
from codequestion import views

urlpatterns = [
    path('', views.index),
    path('update/<str:pk>/', views.update, name="update_question_status"),
    path('search/', views.search, name="search_question")
]