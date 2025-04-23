import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    def show_own_task(self, queryset, arg, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    own_tasks = django_filters.BooleanFilter(
        method='show_own_task',
        widget=forms.CheckboxInput,
        label=_('Show own tasks'),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label filter'),
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
