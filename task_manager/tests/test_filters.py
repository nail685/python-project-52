from django.test import TestCase

from task_manager.tasks.filters import TaskFilter
from task_manager.users.models import User


class FilterTestCase(TestCase):
    fixtures = ["user_test", "label_test", "status_test", "task_test"]

    def login(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_status(self):
        filter_data = {'status': 1}
        filter = TaskFilter(data=filter_data)
        self.assertEqual(filter.qs.count(), 1)
        self.assertEqual(filter.qs.first().status.name, 'online-test')

    def test_executor(self):
        filter_data = {'executor': 1}
        filter = TaskFilter(data=filter_data)
        self.assertEqual(filter.qs.count(), 2)
        self.assertEqual(filter.qs.first().executor.username, 'IvGroz')

    def test_author(self):
        filter_data = {'author': 1}
        filter = TaskFilter(data=filter_data)
        self.assertEqual(filter.qs.count(), 2)
        self.assertEqual(filter.qs.first().author.username, 'IvGroz')