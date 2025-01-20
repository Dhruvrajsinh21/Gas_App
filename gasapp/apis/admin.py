from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_customer_username', 'type_of_service', 'status', 'created_at', 'updated_at')
    search_fields = ('user', 'type_of_service', 'status')
    list_filter = ('status', 'type_of_service', 'created_at')
    ordering = ('-created_at',)  # Orders by the latest requests first
    readonly_fields = ('created_at', 'updated_at')  # Makes timestamps read-only
    fieldsets = (
        (None, {
            'fields': ('user', 'type_of_service', 'description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_customer_username(self, obj):
        return obj.user.username if obj.user else "N/A"
    get_customer_username.short_description = 'Customer Username'
