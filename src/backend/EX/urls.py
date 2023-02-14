"""EX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
Example of CRUD for model Question
    `router = routers.DefaultRouter()`
    `router.register(r'question', views.QuestionViewSet, basename='Question')`
"""
from django.contrib import admin
from django.urls import path, include
from question import views as question_views
from public import views as public_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'question', question_views.QuestionViewSet, basename='Question')
router.register(r'solution', question_views.SolutionViewSet, basename='Solution')
router.register(r'keypoint', question_views.KeypointViewSet, basename='Keypoint')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include((router.urls, 'app_name'))),
    path('', public_views.home, name='home'),
]
