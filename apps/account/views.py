from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import User
from account.forms import AccountUpdateForm


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = 'account_templates/views/account_manage.html'
    success_url = reverse_lazy('account-manage')

    def get_object(self):
        return self.request.user

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account_templates/views/account_delete.html'
    success_url = reverse_lazy('core-home')

    def get_object(self):
        return self.request.user

class AccountProfileView(DetailView):
    model = User
    template_name = 'account_templates/views/account_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])