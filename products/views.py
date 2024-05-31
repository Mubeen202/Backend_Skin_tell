# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *

class CategoriesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Categories.objects.all()
        serializer = CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            serializer = CategoriesSerializer(category)
            return Response(serializer.data)
        except Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            serializer = CategoriesSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()
            return Response({'message': 'Category Deleted Successfully', 'error': False, 'code': 200}, status=status.HTTP_204_NO_CONTENT)
        except Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class ProductsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Products.objects.all()
        serializer = GettingProductsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            serializer = ProductsSerializer(product)
            return Response(serializer.data)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        product_category = request.data['product_category']
        product_name = request.data['product_name']
        
        # Perform a query to check if a record with the given product_category and product_name exists
        category_exists = Products.objects.filter(product_category=product_category, product_name=product_name).exists()
        print('return', category_exists)
        
        # If a matching record exists, return an error response
        if category_exists:
            return Response({'error': 'Category with this product category and product_name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        else:
            serializer = ProductsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            serializer = ProductsSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            product.delete()
            return Response({'message': 'Product Deleted Successfully', 'error': False, 'code': 200}, status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Review.objects.all()
        serializer = GettingReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Review.objects.get(pk=pk)
            serializer = GettingReviewSerializer(product)
            return Response(serializer.data)
        except Products.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            serializer = ProductsSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
            product.delete()
            return Response({'message': 'Review Deleted Successfully', 'error': False, 'code': 200}, status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
