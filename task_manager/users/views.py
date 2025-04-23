from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..mixins import AuthenticationMixin, AuthorizationMixin
from .forms import UserForm
from .models import User


class ListUsers(ListView):
    model = User
    context_object_name = 'users'
    extra_context = {'title': _('Users')}


class SignUpUser(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = 'general/general_form.html'
    extra_context = {'title': _('Registration'), 'button': _("To sign up")}
    success_message = _('User was registered successfully.')


class UpdateUser(
    AuthenticationMixin, AuthorizationMixin, SuccessMessageMixin, UpdateView):
    model = User
    extra_context = {
        'title': _('Changing user'),
        'button': _("Change"),
    }
    form_class = UserForm
    context_object_name = 'update_user'
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('users')
    success_message = _('User was changed successfully')


class DeleteUser(
    AuthenticationMixin, AuthorizationMixin, SuccessMessageMixin, DeleteView):
    model = User
    extra_context = {'title': _('Deleting user'), 'button': _("Yes, delete")}
    template_name = 'general/general_delete_confirm.html'

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _("User was deleted successfully"))
            return redirect(reverse_lazy('users'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Can't delete, user in use")
            )
            return redirect(reverse_lazy('users'))
