from django.test import TestCase

from menu.models import Menu, MenuCategory
from users.models import ClientProfile, User
from .models import Order, OrderItem


class ProtectedOrderPageTests(TestCase):
    def test_anonymous_users_are_redirected_to_login(self):
        for path in ('/orders/', '/checkout/'):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertRedirects(
                    response,
                    f'/auth/?next={path}',
                    fetch_redirect_response=False,
                )


class DynamicOrderPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='customer@example.com',
            password='test-password',
            first_name='Test',
            last_name='Customer',
            role='client',
        )
        self.profile = ClientProfile.objects.create(user=self.user, phone='+255700000001')
        self.category = MenuCategory.objects.create(name='Buns')
        self.menu_item = Menu.objects.create(
            category=self.category,
            name='Dar Coffee Bun',
            price=250,
            image_url='https://example.com/bun.jpg',
            description='Freshly baked coffee bun',
        )
        self.order = Order.objects.create(
            client=self.profile,
            full_name='Test Customer',
            phone='+255700000001',
            street_address='Plot 45, Samora Avenue',
            city='Dar es Salaam',
            postal_code='11101',
            total_price=535,
        )
        OrderItem.objects.create(
            order=self.order,
            menu=self.menu_item,
            quantity=2,
            purchase_price=250,
        )
        self.client.force_login(self.user)

    def test_orders_page_renders_real_order_details(self):
        response = self.client.get('/orders/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, 'Dar Coffee Bun')
        self.assertContains(response, 'Qty: 2')
        self.assertContains(response, 'TSh 500')
        self.assertContains(response, 'TSh 535')
        self.assertNotContains(response, 'Signature Karak Tea')

    def test_orders_page_shows_empty_state_when_customer_has_no_orders(self):
        self.order.delete()

        response = self.client.get('/orders/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have no orders yet.')
