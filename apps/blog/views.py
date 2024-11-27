from calendar import month_name

from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from account.models import User
from argus.permissions import EngilorianRequiredMixin
from category.models import Category, Topic
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogHomeView(TemplateView):
    template_name = 'blog_templates/views/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['spotlighted_post'] = self.get_spotlighted_post()
        context['featured_posts'] = self.get_featured_posts()
        context['recent_posts'] = self.get_recent_posts(context['spotlighted_post'], context['featured_posts'])
        context['engilorians'] = self.get_engilorians()
        context['archives'] = self.get_archives()

        return context

    def get_spotlighted_post(self):
        return BlogPost.objects.filter(is_spotlighted=True, status='published').first()

    def get_featured_posts(self):
        return BlogPost.objects.filter(is_featured=True, status='published').exclude(is_spotlighted=True)[:2]

    def get_recent_posts(self, spotlighted_post, featured_posts):
        excluded_ids = [spotlighted_post.id] if spotlighted_post else []
        excluded_ids += [post.id for post in featured_posts]
        return BlogPost.objects.filter(status='published').exclude(id__in=excluded_ids).order_by('-published_at')[:5]

    def get_engilorians(self):
        return User.objects.filter(is_engilorian=True)

    def get_archives(self):
        from calendar import month_name
        from django.db.models.functions import ExtractYear, ExtractMonth
        from django.db.models import Count

        archives = (
            BlogPost.objects.filter(status='published')
            .annotate(
                year=ExtractYear('published_at'),
                month=ExtractMonth('published_at')
            )
            .values('year', 'month')
            .annotate(post_count=Count('id'))
            .order_by('-year', '-month')
        )

        for archive in archives:
            archive['month_name'] = month_name[archive['month']]

        return archives
    

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_templates/views/blog_list.html'
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
    success_url = reverse_lazy('blog-posts')

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user
