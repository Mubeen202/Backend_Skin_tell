# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('process-payment', views.PaymentView.as_view(), name='process_payment'),
]
