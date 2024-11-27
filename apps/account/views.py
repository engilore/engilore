from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import BlogPost
from account.models import User
from account.forms import AccountUpdateForm


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = 'account_templates/views/account_manage.html'
    success_url = reverse_lazy('account-manage')

    def get_object(self):
        return self.request.user

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account_templates/views/account_delete.html'
    success_url = reverse_lazy('core-home')

    def get_object(self):
        return self.request.user

class AccountProfileView(DetailView):
    model = User
    template_name = 'account_templates/views/account_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_posts(self, profile_user, status_filter):
        if status_filter == 'draft':
            return BlogPost.objects.filter(author=profile_user, status='draft').order_by('-created_at')
        return BlogPost.objects.filter(author=profile_user, status='published').order_by('-published_at')

    def get_filtered_posts(self, profile_user):
        current_user = self.request.user
        status_filter = self.request.GET.get('status', 'published')

        if current_user.is_authenticated and current_user == profile_user and current_user.is_engilorian:
            return self.get_posts(profile_user, status_filter), status_filter, True
        return self.get_posts(profile_user, 'published'), 'published', False

    def paginate_posts(self, posts):
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        posts, current_status, show_drafts = self.get_filtered_posts(profile_user)
        
        page_obj = self.paginate_posts(posts)

        context.update({
            'page_obj': page_obj,
            'posts': page_obj.object_list,
            'current_status': current_status,
            'show_drafts': show_drafts,
        })
        return context