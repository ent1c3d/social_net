from rest_framework import permissions
from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.api import serializers
from posts.api.pagination import PostPagination, LikePagination
from posts.api.serializers import get_like_serializer
from posts.models import Post, Like


class PostCRSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, id=None, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=id)
        serializer = serializers.PostDetailSerializer(post)
        return Response(serializer.data)


class LikeCreateListDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    post_id_qs_param = 'post_id'
    pagination_class = LikePagination

    def perform_create(self, serializer):
        post_id = self.kwargs.get(self.post_id_qs_param)
        serializer.save(user_id=self.request.user.id, post_id=post_id)

    def list(self, request, **kwargs):
        post_id = self.kwargs.get(self.post_id_qs_param)
        queryset = Like.objects.filter(post_id=post_id).order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        post_id = self.kwargs.get(self.post_id_qs_param)
        return get_like_serializer(
            post_id=post_id,
            user=self.request.user
        )
