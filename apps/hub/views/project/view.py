from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from argus.permissions import AdminRequiredMixin

from hub.models import Project
from hub.views.project.form import ProjectForm


class ProjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Project
    template_name = 'hub_templates/views/project/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'hub_templates/views/project/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.all()

class ProjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'hub_templates/views/project/project_create.html'
    success_url = reverse_lazy('list-project')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Project '{form.instance.name}' created successfully.")
        return response

class ProjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'hub_templates/views/project/project_update.html'
    success_url = reverse_lazy('list-project')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Project '{form.instance.name}' updated successfully.")
        return response

class ProjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Project
    template_name = 'hub_templates/views/project/project_delete.html'
    success_url = reverse_lazy('list-project')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Project '{project_name}' has been deleted.")
        return response
