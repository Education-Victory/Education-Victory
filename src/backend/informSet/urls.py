from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from.views import *
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.SimpleRouter()
router.register(r'UserApi', UserViewSet)
router.register(r'UserScoreApi', UserScoreViewSet)
router.register(r'UserFavApi', UserFavViewSet)
urlpatterns = [
    path('ModifyScoreApi/userscore:category=<int:score_category>/', UserScoreModifyApiView.as_view()),
    path('docs/', include_docs_urls(title='Api')),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls