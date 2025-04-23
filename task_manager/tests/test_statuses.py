from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = ["user_test", "status_test"]

    def test_access(self):
        resp1 = self.client.get(reverse('status_create'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('statuses'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)

        self.login()
        resp1 = self.client.get(reverse('status_create'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('statuses'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)

    def login(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_create_status(self):
        self.login()
        resp = self.client.get(reverse('status_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')

        resp = self.client.post(reverse('status_create'), {
            'name': 'test',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('statuses'))
        status = Status.objects.last()
        self.assertEqual(status.name, 'test')

        resp = self.client.get(reverse('statuses'))
        self.assertTrue(len(resp.context['statuses']) == 4)

    def test_ListStatuses(self):
        self.login()
        resp = self.client.get(reverse('statuses'))
        self.assertTrue(len(resp.context['statuses']) == 3)

    def test_UpdateStatus(self):
        self.login()
        status = Status.objects.get(id=1)
        resp = self.client.get(
            reverse('status_update', kwargs={'pk': status.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')
        resp = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}), {
                'name': 'test_status'
            })
        self.assertEqual(resp.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'test_status')

    def test_DeleteStatus(self):
        self.login()
        status = Status.objects.get(name="online-test")
        resp = self.client.get(
            reverse('status_delete', kwargs={'pk': status.id})
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id})
        )
        self.assertRedirects(resp, reverse('statuses'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)
