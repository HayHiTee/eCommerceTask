from django.urls import path

from eCommerceApp.views import CategoryListCreateView, ProductListCreateView, ProductDetailView, DiscountCreateView

urlpatterns = [
    path('categories', CategoryListCreateView.as_view(), name='category'),
    path('products', ProductListCreateView.as_view(), name='product'),
    path('products/<pk>', ProductDetailView.as_view(), name='product_detail'),
    path('discounts', DiscountCreateView.as_view(), name='discount_create'),
]