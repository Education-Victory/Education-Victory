from django.urls import path
from questionaire import views

urlpatterns = [
    path('theme/<str:theme>', views.index, name='questionaire_page'),
    path('home', views.questionaire_selection, name='home'),
    path('success', views.success, name = 'success')
]