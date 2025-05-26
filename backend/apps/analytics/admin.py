from django.contrib import admin
from apps.analytics.models import Analytics


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('total_users', 'total_posts', 'total_likes', 'total_comments', 'total_followers', 'last_updated')
    readonly_fields = [f.name for f in Analytics._meta.fields]
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False