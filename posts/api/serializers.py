from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts.models import Post, Like

User = get_user_model()


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'text',
            'created_at',
            'posted_by',
            'post_author',
            'likes_quan',
            'liked_by_users',
        ]


def get_like_serializer(post_id, user=None):
    class LikesSerializer(serializers.ModelSerializer):
        class Meta:
            model = Like
            fields = [
                'id',
                'created_at',
                'post_id',
                'liked_by',
                'liked_by_name',
            ]

        def validate(self, data):
            post_qs = Post.objects.filter(id=post_id)
            if not post_qs.exists() and post_qs.count() != 1:
                raise ValidationError(f"Can not find the post with id {post_id}")
            like_qs = Like.objects.filter(post=post_id, user=user)
            if like_qs.exists() and like_qs.count() >= 1:
                raise ValidationError("You have already liked the post")
            return data

        def create(self, validated_data):
            like = Like.objects.create(post_id=post_id,
                                       user_id=user.id)
            return like
    return LikesSerializer
