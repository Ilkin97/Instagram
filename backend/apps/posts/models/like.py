from django.db import models
from apps.auth.models import User
from apps.posts.models import Post


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
    
    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"