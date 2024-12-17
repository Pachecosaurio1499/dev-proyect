from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100, default="Sin título")
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True) 

    def __str__(self):
        return f"{self.user.username}: {self.title[:30]}"

    @property
    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_given")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Evita que un usuario le dé más de un like a un mismo post

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"