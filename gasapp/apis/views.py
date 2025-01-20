from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import ServiceRequest, CustomUser
from .tasks import update_request_status
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest
from .forms import ServiceRequestForm 
from django.views import View


class HomeView(generics.GenericAPIView):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and Password are required.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'login.html')


class SignupView(generics.GenericAPIView):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return render(request, 'signup.html')


class DashboardView(generics.GenericAPIView):
    def get(self, request):
        service_requests = ServiceRequest.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'service_requests': service_requests})

class ServiceRequestCreateView(generics.GenericAPIView):
    def get(self, request):
        form = ServiceRequestForm()
        return render(request, 'create_request.html', {'form': form})

    def post(self, request):
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            update_request_status.delay(service_request.id)

            return redirect('/dashboard/')
        return render(request, 'create_request.html', {'form': form})


class ServiceRequestEditView(generics.GenericAPIView):
    def get(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        form = ServiceRequestForm(instance=service_request)
        return render(request, 'edit_request.html', {'form': form, 'service_request': service_request})

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()

            # Celery Task
            update_request_status.delay(service_request.id)

            return redirect('/dashboard/')
        return render(request, 'edit_request.html', {'form': form, 'service_request': service_request})


class ServiceRequestDetailView(generics.GenericAPIView):
    def get(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        return render(request, 'service_request_detail.html', {'service_request': service_request})
