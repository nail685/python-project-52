from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["user_test"]

    def test_signUp(self):
        resp = self.client.get(reverse('user_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')

        resp = self.client.post(reverse('user_create'), {
            'first_name': 'Nikolay',
            'last_name': 'Melnikov',
            'username': 'test',
            'password1': 'Test123@#',
            'password2': 'Test123@#',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))

        user = User.objects.last()
        self.assertEqual(user.first_name, 'Nikolay')
        self.assertEqual(user.last_name, 'Melnikov')
        self.assertEqual(user.username, 'test')

        resp = self.client.get(reverse('users'))
        self.assertTrue(len(resp.context['users']) == 3)

    def test_ListUsers(self):
        resp = self.client.get(reverse('users'))
        self.assertTrue(len(resp.context['users']) == 2)

    def test_UpdateUser(self):
        user = User.objects.get(id=1)
        resp = self.client.get(
            reverse('user_update', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        self.client.force_login(user)
        resp = self.client.get(
            reverse('user_update', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')
        resp = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'first_name': 'Petya',
                'last_name': 'Piter',
                'username': 'Petr1',
                'password1': 'Te1@',
                'password2': 'Te1@',
            }
        )
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Petya')

    def test_DeleteUser(self):
        user = User.objects.get(username="Masha003")
        resp = self.client.get(
            reverse('user_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        self.client.force_login(user)
        resp = self.client.get(
            reverse('user_delete', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('user_delete', kwargs={'pk': user.id})
        )
        self.assertRedirects(resp, reverse('users'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
