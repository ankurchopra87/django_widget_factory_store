from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from store import models

# Create your tests here.


class OrdersApITests(APITestCase):

    base_url = reverse('order-list')

    def setUp(self):
        parent_category = models.ProductCategory.objects.create(
            parent=None, name="category_parent", description="Parent Category")

        child_category = models.ProductCategory.objects.create(
            parent=None, name="category_child", description="Child Category")

        product = models.Product.objects.create(
            name='Product', description='Product 1',
            manufacturer='WidgetFactory', category=child_category
        )

        models.Product.objects.create(
            name='Product 2', description='Product 2',
            manufacturer='WidgetFactory', category=child_category
        )

        models.Product.objects.create(
            name='Product 3', description='Product 3',
            manufacturer='WidgetFactory', category=parent_category
        )

        size_attribute_type = models.AttributeType.objects.create(
            name='Size', description='Size'
        )

        finish_attribute_type = models.AttributeType.objects.create(
            name='Finish', description='Finish'
        )

        small_size_attribute = models.Attribute.objects.create(
            type=size_attribute_type, name='Small', description='Small Size'
        )

        large_size_attribute = models.Attribute.objects.create(
            type=size_attribute_type, name='Large', description='Large Size'
        )

        red_finish_attribute = models.Attribute.objects.create(
            type=finish_attribute_type, name='Red', description='Red Finish'
        )

        sku1 = models.SKU.objects.create(
            number="PR-RD-SM", product=product, price=0.00059, currency='BTC',
            quantity=100
        )

        sku1.attributes.add(small_size_attribute)
        sku1.attributes.add(red_finish_attribute)

        sku2 = models.SKU.objects.create(
            number="PR-RD-LG", product=product, price=0.00059, currency='BTC',
            quantity=100
        )

        sku2.attributes.add(large_size_attribute)
        sku2.attributes.add(red_finish_attribute)

        # bill_to = models.Address.create(
        #     country='USA', street='street1', city='city1',
        #     postal_code='1234', state='state1'
        # )

        # ship_to = models.Address.create(
        #     country='USA', street='street2', city='city2',
        #     postal_code='5678', state='state2'
        # )

        # contact = models.Contact.create(
        #     full_name='Full Name', email='email@example.com')

        # order = models.Order.create(
        #     ship_to=ship_to, bill_to=bill_to, contact=contact
        # )

    def test_POSTing_a_new_order(self):
        post_data = {
            'bill_to': {
                'country': 'USA',
                'street': 'street1',
                'city': 'city1',
                'state': 'state1',
                'postal_code': '1234'
            },
            'ship_to': {
                'country': 'UK',
                'street': 'street2',
                'city': 'city2',
                'state': 'state2',
                'postal_code': '5678'
            },
            'contact': {
                'full_name': 'Full Name',
                'email': 'email@example.com'
            },
            'order_line_set': [
                {
                    'sku': '1',
                    'price': '0.0050',
                    'currency': 'BTC',
                    'quantity': '1',
                    'ordering': '1'
                },
                {
                    'sku': '2',
                    'price': '0.0060',
                    'currency': 'BTC',
                    'quantity': '2',
                    'ordering': '2'
                }
            ]
        }

        response = self.client.post(self.base_url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Order.objects.count(), 1)

        order = models.Order.objects.select_related(
            'ship_to', 'bill_to', 'contact'
        ).prefetch_related(
            Prefetch(
                'order_line_set',
                queryset=models.OrderLine.objects.order_by('id')
            )
        ).get()

        self.assertEqual(order.order_line_set.count(), 2)
        self.assertNotEqual(order.ship_to, None)
        self.assertNotEqual(order.bill_to, None)
        self.assertNotEqual(order.contact, None)

        self.assertEqual(order.contact.full_name, "Full Name")
        self.assertEqual(order.contact.email, "email@example.com")

        self.assertEqual(order.bill_to.country, "USA")
        self.assertEqual(order.bill_to.street, "street1")
        self.assertEqual(order.bill_to.city, "city1")
        self.assertEqual(order.bill_to.state, "state1")
        self.assertEqual(order.bill_to.postal_code, "1234")

        self.assertEqual(order.ship_to.country, "UK")
        self.assertEqual(order.ship_to.street, "street2")
        self.assertEqual(order.ship_to.city, "city2")
        self.assertEqual(order.ship_to.state, "state2")
        self.assertEqual(order.ship_to.postal_code, "5678")

        order_lines = order.order_line_set.all()

        self.assertEqual(order_lines[0].sku_id, 1)
        self.assertEqual(order_lines[0].price, Decimal('0.005'))
        self.assertEqual(order_lines[0].currency, 'BTC')
        self.assertEqual(order_lines[0].quantity, 1)
        self.assertEqual(order_lines[0].ordering, 1)

        self.assertEqual(order_lines[1].sku_id, 2)
        self.assertEqual(order_lines[1].price, Decimal('0.006'))
        self.assertEqual(order_lines[1].currency, 'BTC')
        self.assertEqual(order_lines[1].quantity, 2)
        self.assertEqual(order_lines[1].ordering, 2)

    def test_POSTing_a_new_order_missing_info(self):
        post_data = {
            'bill_to': {
                'country': 'USA',
                'street': 'street1',
                'city': 'city1',
                'state': 'state1',
                'postal_code': '1234'
            },
            'ship_to': {
                'country': 'UK',
                'street': 'street2',
                'city': 'city2',
                'state': 'state2',
                'postal_code': '5678'
            },
            'contact': {
                'full_name': 'Full Name',
                # 'email': 'email@example.com'
            },
            'order_line_set': [
                {
                    'sku': '1',
                    'price': '0.0050',
                    'currency': 'BTC',
                    'quantity': '1',
                    'ordering': '1'
                },
                {
                    'sku': '2',
                    'price': '0.0060',
                    'currency': 'BTC',
                    'quantity': '2',
                    'ordering': '2'
                }
            ]
        }

        response = self.client.post(self.base_url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POSTing_a_new_order_invalid_email(self):
        post_data = {
            'bill_to': {
                'country': 'USA',
                'street': 'street1',
                'city': 'city1',
                'state': 'state1',
                'postal_code': '1234'
            },
            'ship_to': {
                'country': 'UK',
                'street': 'street2',
                'city': 'city2',
                'state': 'state2',
                'postal_code': '5678'
            },
            'contact': {
                'full_name': 'Full Name',
                'email': 'email'
            },
            'order_line_set': [
                {
                    'sku': '1',
                    'price': '0.0050',
                    'currency': 'BTC',
                    'quantity': '1',
                    'ordering': '1'
                },
                {
                    'sku': '2',
                    'price': '0.0060',
                    'currency': 'BTC',
                    'quantity': '2',
                    'ordering': '2'
                }
            ]
        }

        response = self.client.post(self.base_url, post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_GET_products(self):

        url = reverse('product-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
