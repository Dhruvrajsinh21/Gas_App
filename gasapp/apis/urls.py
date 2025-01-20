from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Frontend
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('requests/create/', views.ServiceRequestCreateView.as_view(), name='create_request'),
    path('requests/<int:pk>/edit/', views.ServiceRequestEditView.as_view(), name='edit_request'),
    path('requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='view_request'),
]
