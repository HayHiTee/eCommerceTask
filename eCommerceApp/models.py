import uuid

from django.db import models

# Create your models here.

DISCOUNT_UNITS_CHOICES = (
    ('fixed', 'Fixed Price'),
    ('percent', 'Percentage'),
)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_unit = models.CharField(max_length=10, choices=DISCOUNT_UNITS_CHOICES)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='discounts')


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', null=True, blank=True, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
