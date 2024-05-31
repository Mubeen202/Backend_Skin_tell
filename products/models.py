from django.db import models
from accounts.models import User
# Create your models here.
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(unique=True, max_length=255)
    #after authentication blank false 
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='catagory_created', on_delete=models.CASCADE )
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title


    


class Products(models.Model):
    AVAILABILITY_CHOICES = [
        'S', 'M', 'L', 'XL','2XL'
    ]

    TYPE_CHOICES = [
        'male', 'female', 'unisex'  # Add more types as needed
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name=models.CharField(max_length=255)
    product_category = models.ForeignKey(Categories, null=False, blank=False,  related_name='product_catagory', on_delete=models.CASCADE )
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    link_url=models.CharField(max_length=255)
    product_description=models.TextField()
    product_long_description=models.TextField()
    availability = models.JSONField(default=list)
    type = models.CharField(max_length=10, choices=[(choice, choice) for choice in TYPE_CHOICES])
    
    #after authentication blank false 
    created_by = models.ForeignKey(User, null=True,blank=True, related_name='product_created', on_delete=models.CASCADE )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    in_stock_total=models.IntegerField(default=1)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.product_name
    
    
    
    
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description=models.TextField(max_length=1000)
    #after authentication blank false 
    user_id = models.ForeignKey(User, null=False, blank=False, related_name='user_review_created', on_delete=models.CASCADE )
    product_id = models.ForeignKey(Products, null=False, blank=False, related_name='product_review', on_delete=models.CASCADE )
    rating_number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title