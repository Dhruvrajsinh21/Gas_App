from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import ServiceRequestForm
from .models import ServiceRequest

# Home view
class HomeView(TemplateView):
    template_name = "base.html"

# Create Service Request View
class CreateServiceRequestView(LoginRequiredMixin, FormView):
    template_name = "service_request.html"
    form_class = ServiceRequestForm
    success_url = reverse_lazy('track-requests')  # Redirect after successful submission

    def form_valid(self, form):
        service_request = form.save(commit=False)
        service_request.customer = self.request.user  # Associate the request with the logged-in user
        service_request.save()
        return super().form_valid(form)

# Track Service Requests View
class TrackRequestsView(LoginRequiredMixin, TemplateView):
    template_name = "track_request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get only the logged-in user's service requests
        context['service_requests'] = ServiceRequest.objects.filter(customer=self.request.user)
        return context
