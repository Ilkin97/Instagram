from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register/<slug:slug>/', RegisterView.as_view(), name='register'),
]
