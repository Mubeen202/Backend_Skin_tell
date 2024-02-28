from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    # Add custom fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    # Additional fields if needed

    def __str__(self):
        return self.username
