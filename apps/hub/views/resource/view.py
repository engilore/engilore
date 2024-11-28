from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from argus.permissions import AdminRequiredMixin

from hub.models import Resource
from hub.views.resource.form import ResourceForm


class ResourceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Resource
    template_name = 'hub_templates/views/resource/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 20

    def get_queryset(self):
        return Resource.objects.all().order_by('created_at')

class ResourceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'hub_templates/views/resource/resource_create.html'
    success_url = reverse_lazy('list-resource')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Resource '{form.instance.name}' created successfully.")
        return response

class ResourceUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'hub_templates/views/resource/resource_update.html'
    success_url = reverse_lazy('list-resource')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Resource '{form.instance.name}' updated successfully.")
        return response

class ResourceDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Resource
    template_name = 'hub_templates/views/resource/resource_delete.html'
    success_url = reverse_lazy('list-resource')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        resource_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Resource '{resource_name}' has been deleted.")
        return response
