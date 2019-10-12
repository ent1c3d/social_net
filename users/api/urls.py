from django.urls import re_path, path

from .views import UserCreateAPIView

urlpatterns = [
    re_path(r'^$', UserCreateAPIView.as_view(), name='auth'),
]
