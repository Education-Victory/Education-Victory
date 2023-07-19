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
from django.views.generic import TemplateView
from django.urls import path, include
from question import views as question_views
from public import views as public_views
from common import views as common_views
from rest_framework import routers
from rest_framework.schemas import get_schema_view

# Sets up the viewsets for models and maps them to appropriate URLs using SimpleRouter
router = routers.SimpleRouter()
router.register(r'question', question_views.QuestionViewSet, basename='Question')
router.register(r'solution', question_views.SolutionViewSet, basename='Solution')
router.register(r'category', question_views.CategoryViewSet, basename='Category')
router.register(r'submission', common_views.UserSubmissionViewSet, basename='Submission')

urlpatterns = [
    path('openapi', get_schema_view(
            title="API Documents",
            description="API for all things …",
            version="1.0.0"
        ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/evaluation_simple/', public_views.evaluation_simple),
    path('api/', include((router.urls, 'app_name'))),
    path('', public_views.home, name='home'),
    path('question/<str:question_name>/<str:category_name>/', public_views.question_detail, name='question_detail'),
    path('evaluation/<str:type>/', public_views.evaluation, name='evaluation'),
    path('question/', public_views.question, name='question'),
]
