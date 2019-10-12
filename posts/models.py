from django.conf import settings
from django.db import models


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def posted_by(self):
        user = self.user
        return user.id

    @property
    def post_author(self):
        user = self.user
        return f"{user.first_name} {user.last_name}"

    @property
    def liked_by_users(self):
        filtered_likes = Like.objects.filter(post=self.id).order_by("-created_at")
        users = [like.liked_by for like in filtered_likes]
        return users

    @property
    def likes_quan(self):
        likes_quan = Like.objects.filter(post=self.id).count()
        return likes_quan

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def liked_by(self):
        user = self.user
        return user.id

    @property
    def liked_by_name(self):
        user = self.user
        return f"{user.first_name} {user.last_name}"
