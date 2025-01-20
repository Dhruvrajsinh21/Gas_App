from django.contrib import admin
from .models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type_of_service', 'status', 'created_at', 'updated_at')  # Adjusted to match your model
    search_fields = ['customer__username', 'type_of_service', 'status']
    list_filter = ['status', 'type_of_service']

admin.site.register(ServiceRequest, ServiceRequestAdmin)
