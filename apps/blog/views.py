from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from argus.permissions import EngilorianRequiredMixin
from category.models import Category
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogHomeView(TemplateView):
    template_name = 'blog_templates/views/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spotlighted_post'] = BlogPost.objects.filter(is_spotlighted=True, status='published').first()
        context['featured_posts'] = BlogPost.objects.filter(is_featured=True, status='published').exclude(is_spotlighted=True)[:2]
        context['recent_posts'] = BlogPost.objects.filter(status='published').order_by('-published_at')[:5]
        return context

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_templates/views/blog_list.html'
    context_object_name = 'blogposts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('topics')

class BlogPostCreateView(EngilorianRequiredMixin, LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/views/blog_create.html'
    success_url = reverse_lazy('blog-home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.POST.get('category'):
            kwargs['category_id'] = self.request.POST.get('category')
        return kwargs

    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', 'create_post')
        if action == 'update_topics':
            form = self.get_form()
            for field in ['title', 'content', 'post_type', 'status', 'is_featured', 'is_spotlighted']:
                form.fields[field].required = False
            if form.is_valid():
                return self.render_to_response(self.get_context_data(form=form))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_featured = self.request.POST.get('is_featured') == 'on'
        form.instance.is_spotlighted = self.request.POST.get('is_spotlighted') == 'on'
        return super().form_valid(form)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_templates/views/blog_post.html'
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
    template_name = 'blog_templates/views/blog_update.html'

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('detail-blog-post', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.POST.get('category'):
            kwargs['category_id'] = self.request.POST.get('category')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', 'update_post')
        if action == 'update_topics':
            self.object = self.get_object()
            
            form = self.get_form()
            for field in ['title', 'content', 'post_type', 'status', 'is_featured', 'is_spotlighted']:
                if field in form.fields:
                    form.fields[field].required = False
            if form.is_valid():
                return self.render_to_response(self.get_context_data(form=form))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_featured = self.request.POST.get('is_featured') == 'on'
        form.instance.is_spotlighted = self.request.POST.get('is_spotlighted') == 'on'
        return super().form_valid(form)


class BlogPostDeleteView(EngilorianRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_templates/views/blog_delete.html'
    success_url = reverse_lazy('list-blog-posts')

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user
