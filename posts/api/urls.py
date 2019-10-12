from django.urls import re_path

from posts.api.views import PostCRSet, LikeCreateListDeleteViewSet

urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', PostCRSet.as_view({'get': 'get'}), name='posts'),
    re_path(r'^$', PostCRSet.as_view({'get': 'list', 'post': 'create'}), name='posts'),
    re_path(r'^(?P<post_id>\d+)/likes/$', LikeCreateListDeleteViewSet.as_view({'get': 'list',
                                                                               'post': 'create'}), name='likes'),
]
