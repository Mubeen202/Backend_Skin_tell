import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from rest_framework.views import APIView

# Set your Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=1099,  # Amount in the lowest denomination of the currency
                currency="usd",
                payment_method_types=["card"],  # Accept card payments
            )

            # Retrieve the client secret from the payment intent
            client_secret = payment_intent.client_secret

            # Return the client secret to the frontend
            return JsonResponse({"clientSecret": client_secret})

        except Exception as e:
            # Handle any errors and return a JSON response with the error message
            return JsonResponse({"error": str(e)}, status=500)
