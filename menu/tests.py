from django.test import TestCase

from users.models import User
from .models import Menu, MenuCategory


class MenuManagementTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='test-password',
            first_name='Menu',
            last_name='Admin',
            role='admin',
        )
        self.category = MenuCategory.objects.create(name='Buns')
        self.menu_item = Menu.objects.create(
            category=self.category,
            name='Coffee Bun',
            price=4500,
            image_url='https://example.com/bun.jpg',
            description='Freshly baked',
        )

    def test_menu_manager_requires_admin(self):
        response = self.client.get('/menu_manager/')

        self.assertRedirects(
            response,
            '/auth_admin/?next=/menu_manager/',
            fetch_redirect_response=False,
        )

    def test_admin_can_view_menu_details(self):
        self.client.force_login(self.admin)

        response = self.client.get('/menu_manager/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coffee Bun')
        self.assertContains(response, 'TSh 4500')
        self.assertContains(response, 'Freshly baked')
        self.assertContains(response, f'/update_menu/{self.menu_item.id}/')

    def test_admin_can_create_menu_item(self):
        self.client.force_login(self.admin)

        response = self.client.post('/add_menu/', {
            'name': 'Karak Tea',
            'price': '1800',
            'description': 'Spiced tea',
            'image': 'https://example.com/tea.jpg',
            'category': str(self.category.id),
        })

        self.assertRedirects(response, '/menu_manager/')
        self.assertTrue(Menu.objects.filter(name='Karak Tea', price=1800).exists())

    def test_admin_can_update_menu_item(self):
        self.client.force_login(self.admin)
        other_category = MenuCategory.objects.create(name='Drinks')

        response = self.client.post(f'/update_menu/{self.menu_item.id}/', {
            'name': 'Updated Bun',
            'price': '5200',
            'description': 'Updated description',
            'image': 'https://example.com/updated-bun.jpg',
            'category': str(other_category.id),
        })

        self.assertRedirects(response, '/menu_manager/')
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Updated Bun')
        self.assertEqual(self.menu_item.price, 5200)
        self.assertEqual(self.menu_item.description, 'Updated description')
        self.assertEqual(self.menu_item.image_url, 'https://example.com/updated-bun.jpg')
        self.assertEqual(self.menu_item.category, other_category)

    def test_admin_can_delete_menu_item(self):
        self.client.force_login(self.admin)

        response = self.client.post('/delete_menu/', {'menu_id': self.menu_item.id})

        self.assertRedirects(response, '/menu_manager/')
        self.assertFalse(Menu.objects.filter(id=self.menu_item.id).exists())

    def test_invalid_price_does_not_update_menu(self):
        self.client.force_login(self.admin)

        response = self.client.post(f'/update_menu/{self.menu_item.id}/', {
            'name': 'Updated Bun',
            'price': 'not-a-price',
            'description': 'Updated description',
            'image': 'https://example.com/updated-bun.jpg',
            'category': str(self.category.id),
        })

        self.assertRedirects(response, '/menu_manager/')
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Coffee Bun')
        self.assertEqual(self.menu_item.price, 4500)
