from django_filters import rest_framework as filters

from eCommerceApp.models import Product


class CategoryFilter(filters.FilterSet):
    category = filters.CharFilter(lookup_expr='iexact', field_name='category__name')

    class Meta:
        model = Product
        fields = []
        # fields = ['category', ]
