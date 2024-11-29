from django.shortcuts import render

from blog.models import BlogPost
from hub.models import Project


def core_home(request):
    spotlighted_posts = BlogPost.objects.filter(
        is_spotlighted=True,
        status='published',
        published_at__isnull=False
    ).order_by('-published_at')[:3]
    
    projects = Project.objects.all().order_by('-created_at') 

    return render(request, 'core_templates/views/core_home.html', {
        'spotlighted_posts': spotlighted_posts,
        'projects': projects,
    })


def core_about(request):
    return render(request, 'core_templates/views/core_about.html', {'title': 'About'})


def view_404(request, exception):
    return render(request, 'core_templates/errors/404.html', {'title': 'Not Found'}, status=404,)

def view_500(request):
    return render(request, 'core_templates/errors/500.html', {'title': 'Internal Server Error'}, status=500)

def view_403(request, exception):
    return render(request, 'core_templates/errors/403.html', {'title': 'Forbidden Access'}, status=403)

def view_400(request, exception):
    return render(request, 'core_templates/errors/400.html', {'title': '400'}, status=400)