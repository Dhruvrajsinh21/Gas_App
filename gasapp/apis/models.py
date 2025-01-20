from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    type_of_service = models.CharField(max_length=50)
    details = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_of_service} - {self.status}"
