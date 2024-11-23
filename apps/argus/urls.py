from django.urls import path

from argus import views


urlpatterns = [
    path('register/', views.argus_register, name='argus-register'),
    path('login/', views.argus_login, name='argus-login'),
    path('logout/', views.argus_logout, name='argus-logout'),
]