from django.urls import reverse_lazy

from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from argus.permissions import AdminRequiredMixin
from blog.models import Volume
from blog.views.volume.form import VolumeForm


class VolumeListView(AdminRequiredMixin, ListView):
    model = Volume
    template_name = 'blog_templates/views/volume/volume_list.html'
    context_object_name = 'volumes'
    ordering = ['-number']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


class VolumeCreateView(AdminRequiredMixin, CreateView):
    model = Volume
    form_class = VolumeForm
    template_name = 'blog_templates/views/volume/volume_create.html'
    success_url = reverse_lazy('list-volume')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


class VolumeDetailView(DetailView):
    model = Volume
    template_name = 'blog_templates/views/volume/volume_detail.html'
    context_object_name = 'volume'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class VolumeUpdateView(AdminRequiredMixin, UpdateView):
    model = Volume
    form_class = VolumeForm
    template_name = 'blog_templates/views/volume/volume_update.html'
    success_url = reverse_lazy('list-volume')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

class VolumeDeleteView(AdminRequiredMixin, DeleteView):
    model = Volume
    template_name = 'blog_templates/views/volume/volume_delete.html'
    success_url = reverse_lazy('list-volume')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)