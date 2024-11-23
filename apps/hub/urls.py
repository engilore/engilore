from django.urls import path

from hub import views


urlpatterns = [
    path('', views.HubHomeView.as_view(), name='hub-home'),

    path('users/', views.UserListView.as_view(), name='list-user'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='update-user'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete-user'),
]
