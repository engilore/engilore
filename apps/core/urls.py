from django.urls import path

from hub.views.project.view import ProjectDetailView
from core import views


urlpatterns = [
    path('', views.core_home, name='core-home'),
    path('about/', views.core_about, name='core-about'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='detail-project'),
]
