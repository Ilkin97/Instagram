from django.db import models
from apps.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"