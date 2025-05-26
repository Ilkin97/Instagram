from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Analytics
from .serializers import AnalyticsSerializer


class AnalyticsView(APIView):
    def get(self, request):
        analytics = Analytics.get_analytics()
        serializer = AnalyticsSerializer(analytics)
        return Response(serializer.data)
