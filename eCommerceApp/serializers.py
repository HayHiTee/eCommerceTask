from rest_framework import serializers

from eCommerceApp.models import Category, Product, Discount


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'children')
        read_only_fields = ('children',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock_quantity', 'category', 'created_at')


class ProductWithDiscountSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'price_with_discount', 'stock_quantity', 'category', 'created_at', )

    def get_price_with_discount(self, obj):
        discount_objs = Discount.objects.filter(product=obj)
        price = obj.price
        discounts = [price - (price*discount_obj.discount_price/100) if discount_obj.discount_unit=='percent' else price-discount_obj.discount_price for discount_obj in discount_objs]
        max_discount_price = min(discounts)
        return max_discount_price


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'discount_price', 'discount_unit', 'product')
