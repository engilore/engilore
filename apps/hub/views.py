from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import User
from argus.permissions import AdminRequiredMixin
from category.models import Category, Topic
from hub.forms import UserChangeForm


class HubHomeView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'hub_templates/views/hub_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.count()
        context['categories_count'] = Category.objects.count()
        context['topics_count'] = Topic.objects.count()
        context['first_name'] = self.request.user.first_name
        return context

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'hub_templates/views/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'hub_templates/views/user_update.html'
    success_url = reverse_lazy('list-user')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"User {form.instance.username} updated successfully.")
        return response

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'hub_templates/views/user_delete.html'
    success_url = reverse_lazy('list-user')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        username = self.object.username
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"User {username} has been deleted.")
        return response
    
