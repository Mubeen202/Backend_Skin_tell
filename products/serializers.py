# serializers.py
from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Categories
        fields = [
            'id', 'title', 'created_at','created_by', 'is_active'
        ]

class ProductsSerializer(serializers.ModelSerializer):

    availability = serializers.ListField(
        child=serializers.ChoiceField(choices=Products.AVAILABILITY_CHOICES)
    )

    class Meta:
        model = Products
        fields = [
            'id', 'product_name', 'product_category', 'brand', 'product_max_price', 
            'product_discount_price', 'product_description', 'product_long_description', 
            'availability', 'type', 'created_by', 'created_at', 
            'updated_at', 'in_stock_total', 'is_active'
        ]


class GettingProductsSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    product_category = serializers.StringRelatedField()

    availability = serializers.ListField(
        child=serializers.ChoiceField(choices=Products.AVAILABILITY_CHOICES)
    )

    class Meta:
        model = Products
        fields = [
            'id', 'product_name', 'product_category', 'brand', 'product_max_price', 
            'product_discount_price', 'product_description', 'product_long_description', 
            'availability', 'type', 'created_by', 'created_at', 
            'updated_at', 'in_stock_total', 'is_active'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Review
        fields = '__all__'

class GettingReviewSerializer(serializers.ModelSerializer):
    userId= serializers.StringRelatedField()
    product_id= serializers.StringRelatedField()
    class Meta: 
        model = Review
        fields = '__all__'