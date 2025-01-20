from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import ServiceRequest, CustomUser
from .serializers import ServiceRequestSerializer
from .tasks import update_request_status
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest
from .forms import ServiceRequestForm 
from django.views import View

# Frontend views
class HomeView(generics.GenericAPIView):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        # Render the login page when accessed with GET request
        return render(request, 'login.html')

    def post(self, request):
        # Handle the login form submission when accessed with POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Received username: {username}, password: {password}")  # Debugging line

        if not username or not password:
            messages.error(request, "Username and Password are required.")
            return render(request, 'login.html')  # Return to login page with error message

        # Check if the user exists in the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in if the credentials are correct
            login(request, user)
            return redirect('/dashboard/')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'login.html')  # Return to login page with error message


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
            return redirect('/login/')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return render(request, 'signup.html')


class DashboardView(generics.GenericAPIView):
    def get(self, request):
        # Fetch service requests related to the logged-in user
        service_requests = ServiceRequest.objects.filter(user=request.user)
        
        return render(request, 'dashboard.html', {'service_requests': service_requests})


# API views
class ServiceRequestCreateView(generics.GenericAPIView):
    def get(self, request):
        form = ServiceRequestForm()
        return render(request, 'create_request.html', {'form': form})

    def post(self, request):
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Assign the logged-in user
            service_request.save()
            return redirect('/dashboard/')  # Redirect to dashboard after successful creation
        return render(request, 'create_request.html', {'form': form})


# Edit Request View
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
            return redirect('/dashboard/')  # Redirect to dashboard after successful update
        return render(request, 'edit_request.html', {'form': form, 'service_request': service_request})
    
class ServiceRequestDetailView(generics.GenericAPIView):
    def get(self, request, pk):
        # Get the service request by primary key (pk)
        service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)

        # Render the detail view template with the service request object
        return render(request, 'service_request_detail.html', {'service_request': service_request})