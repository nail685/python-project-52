from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    fixtures = ["user_test", "label_test"]

    def test_access(self):
        resp1 = self.client.get(reverse('label_create'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('labels'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)

        self.login()
        resp1 = self.client.get(reverse('label_create'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('labels'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)

    def login(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_ListLabels(self):
        self.login()
        resp = self.client.get(reverse('labels'))
        self.assertTrue(len(resp.context['labels']) == 2)

    def test_CreateLabel(self):
        self.login()
        resp = self.client.get(reverse('label_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')

        resp = self.client.post(reverse('label_create'), {
            'name': 'test',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('labels'))
        label = Label.objects.last()
        self.assertEqual(label.name, 'test')

        resp = self.client.get(reverse('labels'))
        self.assertTrue(len(resp.context['labels']) == 3)

    def test_UpdateLabel(self):
        self.login()
        label = Label.objects.get(id=1)
        resp = self.client.get(
            reverse('label_update', kwargs={'pk': label.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')
        resp = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}), {
                'name': 'test_label'
            })
        self.assertEqual(resp.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'test_label')

    def test_DeleteLabel(self):
        self.login()
        label = Label.objects.get(name="home-test")
        resp = self.client.get(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
        )
        self.assertRedirects(resp, reverse('labels'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Label.objects.count(), 1)
