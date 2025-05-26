from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from apps.analytics.models import Analytics


User = get_user_model()

@receiver(post_save, sender=User)
def increase_user_count(sender, instance, created, **kwargs):
    if created:
        Analytics.increment("total_users")
