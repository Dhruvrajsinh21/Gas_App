# forms.py
from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['type_of_service', 'description', 'attachment']  # Update with the correct fields from your model
