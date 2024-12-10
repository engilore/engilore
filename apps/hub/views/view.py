from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import User
from argus.permissions import AdminRequiredMixin
from category.models import Category, Topic
from hub.models import Project
from blog.models import Volume


class HubHomeView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'hub_templates/views/hub_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.count()
        context['categories_count'] = Category.objects.count()
        context['topics_count'] = Topic.objects.count()
        context['projects'] = Project.objects.annotate(resource_count=Count('resources'))
        context['projects_count'] = context['projects'].count()
        context['volumes_count'] = Volume.objects.count()
        context['volumes'] = Volume.objects.all().order_by('-number')
        context['first_name'] = self.request.user.first_name
        return context