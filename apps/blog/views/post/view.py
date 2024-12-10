from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from argus.permissions import EngilorianRequiredMixin
from category.models import Category, Topic
from blog.models import BlogPost, Volume
from blog.views.post.form import BlogPostForm
    

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_templates/views/post/blog_list.html'
    context_object_name = 'blogposts'
    paginate_by = 10

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('topics')

        filters = {
            'category': self.request.GET.get('category'),
            'topic': self.request.GET.get('topic'),
            'post_type': self.request.GET.get('post_type'),
            'search_query': self.request.GET.get('q'),
            'start_date': self.request.GET.get('start_date'),
            'end_date': self.request.GET.get('end_date'),
            'year': self.request.GET.get('year'),
            'month': self.request.GET.get('month'),
        }

        return self.apply_filters(queryset, filters)

    def apply_filters(self, queryset, filters):
        if filters['category']:
            queryset = queryset.filter(category__name=filters['category'])
        if filters['topic']:
            queryset = queryset.filter(topics__name=filters['topic'])
        if filters['post_type']:
            queryset = queryset.filter(post_type=filters['post_type'])
        if filters['search_query']:
            queryset = queryset.filter(
                Q(title__icontains=filters['search_query']) |
                Q(meta_description__icontains=filters['search_query'])
            )
        if filters['start_date']:
            parsed_start_date = parse_date(filters['start_date'])
            if parsed_start_date:
                queryset = queryset.filter(published_at__gte=parsed_start_date)
        if filters['end_date']:
            parsed_end_date = parse_date(filters['end_date'])
            if parsed_end_date:
                queryset = queryset.filter(published_at__lte=parsed_end_date)
        if filters['year']:
            queryset = queryset.filter(published_at__year=filters['year'])
        if filters['month']:
            queryset = queryset.filter(published_at__month=filters['month'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context

    def get_extra_context(self):
        return {
            'categories': Category.objects.all(),
            'topics': Topic.objects.all(),
            'post_types': BlogPost.objects.values_list('post_type', flat=True).distinct(),
            'query_params': self.request.GET,
            'selected_year': self.request.GET.get('year'),
            'selected_month': self.request.GET.get('month'),
        }

class BlogPostCreateView(EngilorianRequiredMixin, LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/views/post/blog_create.html'
    success_url = reverse_lazy('blog-home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.POST.get('category'):
            kwargs['category_id'] = self.request.POST.get('category')
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.user.is_admin:
            form.instance.is_featured = self.request.POST.get('is_featured') == 'on'
            form.instance.is_spotlighted = self.request.POST.get('is_spotlighted') == 'on'
        else:
            form.instance.is_featured = False
            form.instance.is_spotlighted = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['volumes'] = Volume.objects.all()
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_templates/views/post/blog_post.html'
    context_object_name = 'blogpost'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(status='published')

    def get_object(self, queryset=None):
        blog_post = super().get_object(queryset)
        if blog_post.status != 'published' and blog_post.author != self.request.user:
            raise HttpResponseForbidden("You do not have permission to view this blog post.")
        return blog_post


class BlogPostUpdateView(EngilorianRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/views/post/blog_update.html'

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user or self.request.user.is_admin

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.POST.get('category'):
            kwargs['category_id'] = self.request.POST.get('category')
        else:
            kwargs['category_id'] = self.object.category_id 
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_admin:
            form.instance.is_featured = self.request.POST.get('is_featured') == 'on'
            form.instance.is_spotlighted = self.request.POST.get('is_spotlighted') == 'on'
        else:
            form.instance.is_featured = self.object.is_featured
            form.instance.is_spotlighted = self.object.is_spotlighted
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail-blog-post', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['volumes'] = Volume.objects.all()
        return context


class BlogPostDeleteView(EngilorianRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_templates/views/post/blog_delete.html'
    success_url = reverse_lazy('blog-posts')

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user