# payments/models.py

from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.CharField(max_length=10, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
