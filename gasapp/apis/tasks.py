from celery import shared_task
from django.utils import timezone
from .models import ServiceRequest
from django.core.mail import send_mail  # Optional: For sending email notifications to customers

@shared_task
def update_request_status(request_id, status):
    try:
        # Fetch the ServiceRequest object using the provided request_id
        service_request = ServiceRequest.objects.get(id=request_id)

        # Update the status of the service request
        service_request.status = status
        service_request.resolved_at = timezone.now() if status == 'Resolved' else None
        service_request.save()

        # Optional: Send an email notification to the customer (for status updates)
        send_status_update_email(service_request.user.email, status, service_request.id)

        return f"ServiceRequest {request_id} status updated to {status}"

    except ServiceRequest.DoesNotExist:
        return f"ServiceRequest {request_id} does not exist"

def send_status_update_email(user_email, status, request_id):
    """Send an email notification to the customer regarding the request status update."""
    subject = f"Your Service Request #{request_id} Status Update"
    message = f"Dear Customer,\n\nYour service request #{request_id} has been updated to the following status: {status}.\n\nThank you for using our service."
    send_mail(subject, message, 'no-reply@myapp.com', [user_email])
