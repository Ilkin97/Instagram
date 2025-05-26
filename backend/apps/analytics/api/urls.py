from django.urls import path
from .views import AnalyticsView

urlpatterns = [
    path('api/analytics/', AnalyticsView.as_view(), name='analytics-api'),
]
