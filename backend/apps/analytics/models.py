from django.db import models
from django.utils.timezone import now


class Analytics(models.Model):
    total_users = models.PositiveIntegerField(default=0)
    total_posts = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_followers = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'

    def __str__(self):
        return f"Analytics as of {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"

    def update_totals(self, users=None, posts=None, likes=None, comments=None, followers=None):
        if users is not None:
            self.total_users = users
        if posts is not None:
            self.total_posts = posts
        if likes is not None:
            self.total_likes = likes
        if comments is not None:
            self.total_comments = comments
        if followers is not None:
            self.total_followers = followers
        self.save()

    @classmethod
    def get_analytics(cls):
        return cls.objects.first()

    @classmethod
    def create_or_get(cls):
        analytics, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'total_users': 0,
                'total_posts': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_followers': 0,
            }
        )
        return analytics

    @classmethod
    def reset_analytics(cls):
        analytics = cls.create_or_get()
        analytics.update_totals(0, 0, 0, 0, 0)
        return analytics

    @classmethod
    def increment(cls, field_name):
        analytics = cls.create_or_get()
        if hasattr(analytics, field_name):
            current = getattr(analytics, field_name)
            setattr(analytics, field_name, current + 1)
            analytics.save()
        else:
            raise AttributeError(f"{field_name} is not a valid field")

    @classmethod
    def decrement(cls, field_name):
        analytics = cls.create_or_get()
        if hasattr(analytics, field_name):
            current = getattr(analytics, field_name)
            if current > 0:
                setattr(analytics, field_name, current - 1)
                analytics.save()
            else:
                raise ValueError(f"{field_name} cannot be less than zero")
        else:
            raise AttributeError(f"{field_name} is not a valid field")
