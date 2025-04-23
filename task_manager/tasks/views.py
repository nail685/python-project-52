from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from ..mixins import AuthenticationMixin, AuthorizationTaskMixin
from .filters import TaskFilter
from .models import Task


class TaskMixin(AuthenticationMixin, SuccessMessageMixin):
    model = Task
    extra_context = {'title': _("Tasks"), 'button': _("Create task")}
    success_url = reverse_lazy('tasks')
    fields = ['name', 'description', 'status', 'executor', 'labels']


class ListTask(TaskMixin, FilterView):
    context_object_name = 'tasks'
    extra_context = {'title': _("Tasks"), 'button': _("Create task")}
    template_name = 'tasks/task_list.html'
    filterset_class = TaskFilter


class CreateTask(TaskMixin, CreateView):
    success_message = _("Task created successfully")
    extra_context = {'title': _("Create task"), 'button': _("Create")}
    template_name = 'general/general_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ViewTask(TaskMixin, DetailView):
    context_object_name = 'task'
    extra_context = {'title': _('Show task')}


class UpdateTask(TaskMixin, UpdateView):
    success_message = _("Task edited successfully")
    extra_context = {'title': _('Changing task'), 'button': _('Change')}
    template_name = 'general/general_form.html'


class DeleteTask(TaskMixin, AuthorizationTaskMixin, DeleteView):
    extra_context = {'title': _('Deleting task'), 'button': _('Yes, delete')}
    success_message = _('Task successfully deleted')
    template_name = 'general/general_delete_confirm.html'