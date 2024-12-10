from calendar import month_name

from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.views.generic import TemplateView

from account.models import User
from blog.models import BlogPost, Volume


class BlogHomeView(TemplateView):
    template_name = 'blog_templates/views/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['spotlighted_post'] = self.get_spotlighted_post()
        context['featured_posts'] = self.get_featured_posts()
        context['recent_posts'] = self.get_recent_posts(context['spotlighted_post'], context['featured_posts'])
        context['engilorians'] = self.get_engilorians()
        context['archives'] = self.get_archives()
        context['volumes'] = Volume.objects.all()

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