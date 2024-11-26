from django.shortcuts import render

from blog.models import BlogPost


def core_home(request):
    spotlighted_posts = BlogPost.objects.filter(
        is_spotlighted=True,
        status='published',
        published_at__isnull=False
    ).order_by('-published_at')[:3]
    return render(request, 'core_templates/views/core_home.html', {'spotlighted_posts': spotlighted_posts})

def core_about(request):
    return render(request, 'core_templates/views/core_about.html', {'title': 'About'})
