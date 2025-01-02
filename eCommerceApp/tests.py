from decimal import Decimal
from uuid import UUID

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from eCommerceApp.models import Category, Product, Discount


# Create your tests here.
class CategoryTestCase(APITestCase):
    def test_create_category(self):
        url = reverse('categories')
        name = 'Test Category'
        description = 'Test Description'
        data = {
            'name': name,
            'description': description,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, name)
        self.assertEqual(Category.objects.get().description, description)

    def test_get_all_categories(self):
        url = reverse('categories')
        name = 'Test Category'
        description = 'Test Description'
        data = {
            'name': name,
            'description': description,
        }
        response_create = self.client.post(url, data, format='json')
        response_get = self.client.get(url, format='json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        results = [{
            'id': response_create.data['id'],
            'name': name,
            'description': description,
            'parent': None,
            'children': []
        }]
        self.assertEqual(response_get.data['results'], results)
        self.assertEqual(len(response_get.data['results']), 1)


class ProductTestCase(APITestCase):
    def setUp(self):
        url = reverse('categories')
        name = 'Test Category'
        description = 'Test Description'
        data = {
            'name': name,
            'description': description,
        }
        response = self.client.post(url, data, format='json')
        self.category_id = response.data['id']

    def test_create_product(self):
        url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, name)
        self.assertEqual(Product.objects.get().description, description)
        self.assertEqual(Product.objects.get().price, price)
        self.assertEqual(Product.objects.get().stock_quantity, stock_quantity)
        self.assertEqual(str(Product.objects.get().category.id), self.category_id)

    def test_get_all_products(self):
        url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        response_create = self.client.post(url, data, format='json')

        response_get = self.client.get(url, format='json')

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        results = [{
            'id': response_create.data['id'],
            'name': name,
            'description': description,
            'price': response_create.data['price'],
            'stock_quantity': stock_quantity,
            'category': UUID(self.category_id),
            'created_at': response_create.data['created_at'],
        }]

        self.assertEqual(response_get.data['results'], results)
        self.assertEqual(len(response_get.data['results']), 1)

    def test_get_product(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        response_create = self.client.post(product_create_url, data, format='json')
        product_id = response_create.data['id']

        url = reverse('product_detail', kwargs={'pk': product_id})
        response = self.client.get(url, format='json')
        result = {
            'id': response_create.data['id'],
            'name': name,
            'description': description,
            'price': response_create.data['price'],
            'price_with_discount': '60.00',
            'stock_quantity': stock_quantity,
            'category': UUID(self.category_id),
            'created_at': response_create.data['created_at'],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data, result)

    def test_get_product_with_fixed_discount(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        product_create_response = self.client.post(product_create_url, data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']
        discount_create_url = reverse('discount_create')
        discount_create_data = {
            'product': product_id,
            'discount_price': 20,
            'discount_unit': 'fixed'
        }

        discount_create_response = self.client.post(discount_create_url, discount_create_data, format='json')
        self.assertEqual(discount_create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})
        product_detail_response = self.client.get(product_detail_url, format='json')
        self.assertEqual(product_detail_response.status_code, status.HTTP_200_OK)

        result = {
            'id': product_create_response.data['id'],
            'name': name,
            'description': description,
            'price': product_create_response.data['price'],
            'price_with_discount': '40.00',
            'stock_quantity': stock_quantity,
            'category': UUID(self.category_id),
            'created_at': product_create_response.data['created_at'],
        }

        self.assertEqual(product_detail_response.data, result)

    def test_get_product_with_percent_discount(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        product_create_response = self.client.post(product_create_url, data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']
        discount_create_url = reverse('discount_create')
        discount_create_data = {
            'product': product_id,
            'discount_price': 20,
            'discount_unit': 'percent'
        }

        discount_create_response = self.client.post(discount_create_url, discount_create_data, format='json')
        self.assertEqual(discount_create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})
        product_detail_response = self.client.get(product_detail_url, format='json')
        self.assertEqual(product_detail_response.status_code, status.HTTP_200_OK)

        result = {
            'id': product_create_response.data['id'],
            'name': name,
            'description': description,
            'price': product_create_response.data['price'],
            'price_with_discount': '48.00',
            'stock_quantity': stock_quantity,
            'category': UUID(self.category_id),
            'created_at': product_create_response.data['created_at'],
        }

        self.assertEqual(product_detail_response.data, result)

    def test_get_product_with_multiple_discounts(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        product_create_response = self.client.post(product_create_url, data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']
        discount_create_url = reverse('discount_create')
        discount_create_data = {
            'product': product_id,
            'discount_price': 20,
            'discount_unit': 'percent'
        }

        discount_create_response = self.client.post(discount_create_url, discount_create_data, format='json')
        self.assertEqual(discount_create_response.status_code, status.HTTP_201_CREATED)
        discount_two_create_data = {
            'product': product_id,
            'discount_price': 20,
            'discount_unit': 'fixed'
        }

        discount_two_create_response = self.client.post(discount_create_url, discount_two_create_data, format='json')
        self.assertEqual(discount_two_create_response.status_code, status.HTTP_201_CREATED)

        discount_three_create_data = {
            'product': product_id,
            'discount_price': 30,
            'discount_unit': 'fixed'
        }
        discount_three_create_response = self.client.post(discount_create_url, discount_three_create_data,
                                                          format='json')
        self.assertEqual(discount_three_create_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Discount.objects.count(), 3)

        self.assertEqual(Product.objects.count(), 1)

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})
        product_detail_response = self.client.get(product_detail_url, format='json')
        self.assertEqual(product_detail_response.status_code, status.HTTP_200_OK)

        result = {
            'id': product_create_response.data['id'],
            'name': name,
            'description': description,
            'price': product_create_response.data['price'],
            'price_with_discount': '30.00',
            'stock_quantity': stock_quantity,
            'category': UUID(self.category_id),
            'created_at': product_create_response.data['created_at'],
        }

        self.assertEqual(product_detail_response.data, result)

    def test_put_product_update(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        category = self.category_id

        product_create_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_create_response = self.client.post(product_create_url, product_create_data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})

        product_update_data = {
            'name': name,
            'description': 'New Description',
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_detail_response = self.client.put(product_detail_url, product_update_data, format='json')
        self.assertEqual(product_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        result = {
            'id': product_id,
            'name': name,
            'description': 'New Description',
            'price': str(round(Decimal(price), 2)),
            'price_with_discount': str(round(Decimal(price), 2)),
            'stock_quantity': stock_quantity,
            'category': UUID(category),
            'created_at': product_create_response.data['created_at'],
        }

        self.assertEqual(product_detail_response.data, result)

    def test_patch_product_update(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        category = self.category_id

        product_create_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_create_response = self.client.post(product_create_url, product_create_data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})

        product_update_data = {
            'name': name,
            'description': 'New Description',
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_detail_response = self.client.patch(product_detail_url, product_update_data, format='json')
        self.assertEqual(product_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        result = {
            'id': product_id,
            'name': name,
            'description': 'New Description',
            'price': str(round(Decimal(price), 2)),
            'price_with_discount': str(round(Decimal(price), 2)),
            'stock_quantity': stock_quantity,
            'category': UUID(category),
            'created_at': product_create_response.data['created_at'],
        }

        self.assertEqual(product_detail_response.data, result)

    def test_delete_product(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        category = self.category_id

        product_create_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_create_response = self.client.post(product_create_url, product_create_data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        product_id = product_create_response.data['id']

        product_detail_url = reverse('product_detail', kwargs={'pk': product_id})

        product_delete_response = self.client.delete(product_detail_url, format='json')

        self.assertEqual(product_delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_product_list_by_filter_category(self):
        product_create_url = reverse('products')
        name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        category = self.category_id

        product_create_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category
        }

        product_create_response = self.client.post(product_create_url, product_create_data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        category_url = reverse('categories')
        category_name_two = 'Test Category 2'
        category_description_two = 'Test Description 2'
        category_data_two = {
            'name': category_name_two,
            'description': category_description_two,
        }
        category_response_two = self.client.post(category_url, category_data_two, format='json')
        self.assertEqual(category_response_two.status_code, status.HTTP_201_CREATED)
        category_id_two = category_response_two.data['id']

        product_two_create_data = {
            'name': 'Test Product 2',
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': category_id_two
        }

        product_two_create_response = self.client.post(product_create_url, product_two_create_data, format='json')
        self.assertEqual(product_two_create_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Product.objects.count(), 2)

        query_params_url = f"{reverse('products')}?category={category_name_two}"

        query_params_response = self.client.get(query_params_url, format='json')
        self.assertEqual(query_params_response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(query_params_response.data['results']), 1)


class DiscountTestCase(APITestCase):
    def setUp(self):
        category_url = reverse('categories')
        name = 'Test Category'
        description = 'Test Description'
        data = {
            'name': name,
            'description': description,
        }
        category_response = self.client.post(category_url, data, format='json')
        self.category_id = category_response.data['id']

        product_url = reverse('products')
        product_name = 'Test Product'
        description = 'Test Description'
        price = 60.00
        stock_quantity = 10
        product_data = {
            'name': product_name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity,
            'category': self.category_id
        }

        product_create_response = self.client.post(product_url, product_data, format='json')
        self.assertEqual(product_create_response.status_code, status.HTTP_201_CREATED)

        self.product_id = product_create_response.data['id']

    def test_create_discount(self):
        discount_create_url = reverse('discount_create')
        discount_create_data = {
            'product': self.product_id,
            'discount_price': 30,
            'discount_unit': 'fixed'}

        response = self.client.post(discount_create_url, discount_create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discount.objects.count(), 1)

    def test_get_discounts(self):
        discount_create_url = reverse('discount_create')
        discount_create_data_one = {
            'product': self.product_id,
            'discount_price': 30,
            'discount_unit': 'fixed'}

        discount_create_data_two = {
            'product': self.product_id,
            'discount_price': 30,
            'discount_unit': 'fixed'}

        response_one = self.client.post(discount_create_url, discount_create_data_one, format='json')
        self.assertEqual(response_one.status_code, status.HTTP_201_CREATED)
        response_two = self.client.post(discount_create_url, discount_create_data_two, format='json')
        self.assertEqual(response_two.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discount.objects.count(), 2)
