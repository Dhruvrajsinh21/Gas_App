from celery import shared_task
from .models import ServiceRequest

@shared_task
def update_request_status(request_id):
    """
    Update the status of a service request to 'In Progress' after it is created.
    """
    try:
        request = ServiceRequest.objects.get(id=request_id)
        if request.status == 'Pending':
            request.status = 'In Progress'
            request.save()
    except ServiceRequest.DoesNotExist:
        return "Request not found"
