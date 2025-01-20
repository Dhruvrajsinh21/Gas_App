from django.urls import path
from .views import HomeView, CreateServiceRequestView, TrackRequestsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create-service/', CreateServiceRequestView.as_view(), name='create-service'),
    path('track-requests/', TrackRequestsView.as_view(), name='track-requests'),
]
