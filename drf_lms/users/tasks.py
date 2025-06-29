from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from users.models import CustomUser

@shared_task
def deactivate_inactive_users():
    threshold = now() - timedelta(days=30)
    users = CustomUser.objects.filter(is_active=True, last_login__lt=threshold)
    users.update(is_active=False)
