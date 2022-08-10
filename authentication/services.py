from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def create_dev_user(*args, **kwargs):
    if settings.DEBUG:
        payload = {
            "email": "admin@admin.com",
            "username": "admin",
            "password": "admin",
            "first_name": "Admin",
            "last_name": "Adminovich",
            "age": 1,
            "phone": "063063063",
        }
        User.objects.create_superuser(**payload)
