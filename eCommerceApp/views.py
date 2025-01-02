from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from eCommerceApp.filterset import CategoryFilter
from eCommerceApp.models import Category, Product, Discount
from eCommerceApp.serializers import CategorySerializer, ProductSerializer, DiscountSerializer, \
    ProductWithDiscountSerializer


# Create your views here.

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category',]
    filterset_class = CategoryFilter


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithDiscountSerializer


class DiscountCreateView(ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
