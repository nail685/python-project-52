from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..mixins import AuthenticationMixin
from .models import Status


class StatusMixin(AuthenticationMixin, SuccessMessageMixin):
    model = Status
    extra_context = {'title': _("Statuses"), 'button': _("Create status")}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses')
    fields = ['name']

    
class ListStatuses(StatusMixin, ListView):
    context_object_name = 'statuses'


class CreateStatus(StatusMixin, CreateView):
    success_message = _("Status created successfully")
    extra_context = {'title': _("Create status"), 'button': _("Create")}
    template_name = 'general/general_form.html'


class UpdateStatus(StatusMixin, UpdateView):
    success_message = _("Status changed successfully")
    template_name = 'general/general_form.html'
    extra_context = {'title': _('Changing status'), 'button': _('Change')}


class DeleteStatus(StatusMixin, DeleteView):
    template_name = 'general/general_delete_confirm.html'
    extra_context = {'title': _('Deleting status'), 'button': _('Yes, delete')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _("Status was deleted successfully"))
            return redirect(reverse_lazy('statuses'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Can't delete, status in use")
            )
            return redirect(reverse_lazy('statuses'))