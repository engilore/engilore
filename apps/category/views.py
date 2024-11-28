from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from argus.permissions import AdminRequiredMixin
from category.models import Category, Topic
from category.forms import CategoryForm, TopicForm


class CategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Category
    template_name = 'hub_templates/views/category/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

class CategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'hub_templates/views/category/category_create.html'
    success_url = reverse_lazy('list-category')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Category '{form.instance.name}' created successfully.")
        return response

class CategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'hub_templates/views/category/category_update.html'
    success_url = reverse_lazy('list-category')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Category '{form.instance.name}' updated successfully.")
        return response

class CategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'hub_templates/views/category/category_delete.html'
    success_url = reverse_lazy('list-category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Category '{category_name}' has been deleted.")
        return response


class TopicListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Topic
    template_name = 'hub_templates/views/topic/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 20

class TopicCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'hub_templates/views/topic/topic_create.html'
    success_url = reverse_lazy('list-topic')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Topic '{form.instance.name}' created successfully.")
        return response

class TopicUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'hub_templates/views/topic/topic_update.html'
    success_url = reverse_lazy('list-topic')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Topic '{form.instance.name}' updated successfully.")
        return response


class TopicDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Topic
    template_name = 'hub_templates/views/topic/topic_delete.html'
    success_url = reverse_lazy('list-topic')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        topic_name = self.object.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Topic '{topic_name}' has been deleted.")
        return response