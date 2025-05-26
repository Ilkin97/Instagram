from rest_framework import serializers
from apps.analytics.models import Analytics


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = "__all__"
