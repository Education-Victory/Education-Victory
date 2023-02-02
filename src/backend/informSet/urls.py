from django.urls import re_path
from django.urls import path, include

from.views import(
    WebUserListApiView,
    
)

urlpatterns = [
    path('api', WebUserListApiView.as_view())
]