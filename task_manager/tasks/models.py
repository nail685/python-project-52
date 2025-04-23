from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name=_('Task name'))
    description = models.TextField(
        max_length=1000, blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        null=True,
        blank=True,
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label,
        related_name="label",
        blank=True,
        through='TaskRelationLabel',
        through_fields=('task', 'label'),
        verbose_name=_('Labels'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("=Task=")
        verbose_name_plural = _("=Tasks=")


class TaskRelationLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)