from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..mixins import AuthenticationMixin
from .models import Label


class LabelMixin(AuthenticationMixin, SuccessMessageMixin):
    model = Label
    extra_context = {'title': _("Labels"), 'button': _("Create label")}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')
    fields = ['name']

    
class ListLabels(LabelMixin, ListView):
    context_object_name = 'labels'


class CreateLabel(LabelMixin, CreateView):
    success_message = _("Label created successfully")
    extra_context = {'title': _("Create label"), 'button': _("Create")}
    template_name = 'general/general_form.html'


class UpdateLabel(LabelMixin, UpdateView):
    success_message = _("Label changed successfully")
    template_name = 'general/general_form.html'
    extra_context = {'title': _('Changing label'), 'button': _('Change')}


class DeleteLabel(LabelMixin, DeleteView):
    template_name = 'general/general_delete_confirm.html'
    extra_context = {'title': _('Deleting label'), 'button': _('Yes, delete')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _("Label was deleted successfully"))
            return redirect(reverse_lazy('labels'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Can't delete, label in use")
            )
            return redirect(reverse_lazy('labels'))