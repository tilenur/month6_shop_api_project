from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
from rest_framework import status
from django.db import transaction

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,  # we adjusted from count -> total using Custom class
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all() # list of data from DB
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return CategorySerializer

# @api_view(['GET', 'POST'])
# def category_list_api_view(request):
#     if request.method == "GET":
#         # step 1: (QuerySet)
#         categories = Category.objects.all()
#
#         # step 2: serializer (many=True)
#         data = CategorySerializer(categories, many=True).data
#         # step 3: return response
#         return Response(
#             data=data
#         )
#     elif request.method == "POST":
#         # step 0: Validation (Existing, Typing, Extra)
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # step 1: recieve data
#         name = serializer.validated_data.get("name")
#
#         # step 2: create category
#         category = Category.objects.create(
#             name = name,
#         )
#
#         # step 3: return response
#         return Response(
#             status=status.HTTP_201_CREATED,
#             #show data after posting
#             data=CategorySerializer(category, many=False).data
#         )

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all() # list of data from DB
    serializer_class = CategorySerializer

    # redundant here because DRF already uses pk by default
    # necessary only when URL uses <int:id>
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryValidateSerializer
        return CategorySerializer


# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except:
#         return Response(data={'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         data = CategorySerializer(category, many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         # step 0: Validation (Existing, Typing, Extra)
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # step 1: recieve validated data
#         category.name = serializer.validated_data.get('name')
#         # step 2: update existing object
#         category.save()
#         # step 3: return response
#         return Response(
#             status=status.HTTP_200_OK,
#             data=CategorySerializer(category, many=False).data
#         )

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    # redundant here because DRF already uses pk by default
    # necessary only when URL uses <int:id>
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method in  ["POST", "PUT", "PATCH"]:
            return ProductValidateSerializer
        return ProductSerializer

# @api_view(['GET', 'POST'])
# def product_list_api_view(request):
#     if request.method == 'GET':
#         products = (Product.objects.select_related('category')
#                     .prefetch_related('reviews').all())
#         # products = Product.objects.all()
#         data = ProductSerializer(products, many=True).data
#         return Response(data=data)
#     elif request.method == 'POST':
#         # step 0: Validation (Existing, Typing, Extra)
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # step 1: recieve data
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         price = serializer.validated_data.get('price')
#         category_id = serializer.validated_data.get('category_id')
#
#         # step 2: create product
#         product = Product.objects.create(
#             title = title,
#             description = description,
#             price = price,
#             category_id = category_id,
#         )
#
#         # step 3: return response:
#         return Response(
#             status=status.HTTP_201_CREATED,
#             data=ProductSerializer(product, many=False).data
#         )
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except:
#         return Response(data={'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         data = ProductSerializer(product, many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )
#     elif request.method == 'PUT':
#         # step 0: Validation
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # step 1: Recieve validated data
#         product.title = serializer.validated_data.get('title')
#         product.description = serializer.validated_data.get('description')
#         product.price = serializer.validated_data.get('price')
#         product.category_id = serializer.validated_data.get('category_id')
#         # step 2: update existing object
#         product.save()
#         # step 3: return response
#         return Response(
#             status=status.HTTP_200_OK,
#             data=ProductSerializer(product, many=False).data
#         )

class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all() # list of data from db
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer
        return ReviewSerializer

# @api_view(['GET', 'POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         # step 1: collect reviews
#         reviews = Review.objects.all()
#         # step 2: reformat
#         data = ReviewSerializer(reviews, many=True).data
#         # step 3: return response
#         return Response(data=data)
#     elif request.method == 'POST':
#         #step 0: Validation (Existing, Typing, Extra)
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # step 1: recieve data
#         text = serializer.validated_data.get('text')
#         stars = serializer.validated_data.get('stars')
#         product_id = serializer.validated_data.get('product_id')
#
#         # step 2: create review
#         review = Review.objects.create(
#             text = text,
#             stars = stars,
#             product_id = product_id,
#         )
#
#         # step 3: return response
#         return Response(
#             status=status.HTTP_201_CREATED,
#             data=ReviewSerializer(review, many=False).data
#         )

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # redundant here because DRF already uses pk by default
    # necessary only when URL uses <int:id>
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ReviewValidateSerializer
        return ReviewSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, pk):
#     try:
#         review = Review.objects.get(pk=pk)
#     except:
#         return Response(data={'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         data = ReviewSerializer(review, many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         # step 0: Validate data
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # step 1: recieve validated data
#         review.text = serializer.validated_data.get('text')
#         review.stars = serializer.validated_data.get('stars')
#         review.product_id = serializer.validated_data.get('product_id')
#         # step 2: update object
#         review.save()
#         # step 3: return response
#         return Response(
#             status=status.HTTP_200_OK,
#             data=ReviewSerializer(review, many=False).data
#         )