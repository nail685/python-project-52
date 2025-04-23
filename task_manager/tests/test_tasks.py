from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    fixtures = ["user_test", "label_test", "status_test", "task_test"]

    def test_access(self):
        resp1 = self.client.get(reverse('task_create'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('tasks'))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)
        resp1 = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 302)

        self.login()
        resp1 = self.client.get(reverse('task_create'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('tasks'))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)
        resp1 = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(resp1.status_code, 200)

    def login(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_TaskCreate(self):
        self.login()
        resp = self.client.get(reverse('task_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')

        resp = self.client.post(reverse('task_create'), {
            'name': 'Hard work',
            'description': 'Hard work every day',
            'status': 'Well done',
            'executor': 'Ivan',
            'labels': 'Red flag',
            'author': 'Gamer'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('tasks'))

        task = Task.objects.last()
        self.assertEqual(task.name, 'Hard work')
        self.assertEqual(task.status.name, 'Well done')
        self.assertEqual(task.author.username, 'Ivan')

        resp = self.client.get(reverse('tasks'))
        self.assertTrue(len(resp.context['tasks']) == 3)

    def test_ListTasks(self):
        self.login()
        resp = self.client.get(reverse('tasks'))
        self.assertTrue(len(resp.context['tasks']) == 2)

    def test_ViewTask(self):
        self.login()
        task = Task.objects.get(id=1)
        resp = self.client.get(reverse('task_view', kwargs={'pk': task.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='task/task_detail.html')
        self.assertEqual(task.name, 'Hard work')
        self.assertEqual(task.description, 'Ward work every day')
        self.assertEqual(task.status.name, 'Well done')
        self.assertEqual(task.executor.username, 'Ivan')
        self.assertEqual(task.author.username, 'IvGroz')

    def test_UpdateTask(self):
        self.login()
        task = Task.objects.get(id=1)
        resp = self.client.get(
            reverse('task_update', kwargs={'pk': task.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='general/general_form.html')
        resp = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            {
                'name': 'Do something',
                'description': ' ',
                'status': 2,
                'executor': 2,
                'labels': 2,
            })
        self.assertEqual(resp.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Do something')
        self.assertEqual(task.status.name, 'Medium rear')
        self.assertEqual(task.executor.username, 'Ivan')

    def test_DeleteTask(self):
        self.login()
        task = Task.objects.get(name="test")
        resp = self.client.get(
            reverse('task_delete', kwargs={'pk': task.id})
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id})
        )
        self.assertRedirects(resp, reverse('tasks'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
