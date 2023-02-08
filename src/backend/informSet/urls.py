from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'UserApi', UserViewSet)
router.register(r'UserScoreApi', UserScoreViewSet)
router.register(r'UserFavApi', UserFavViewSet)
#router.register(r'ModifyScoreApi')

urlpatterns = [
    path('ModifyScoreApi/userscore:category=<int:score_category>/', UserScoreModifyApiView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls