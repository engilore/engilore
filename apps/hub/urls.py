from django.urls import path

from hub.views.view import HubHomeView

from hub.views.user.view import (
    UserListView,
    UserUpdateView, 
    UserDeleteView
)

from hub.views.project.view import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)

from hub.views.resource.view import (
    ResourceListView,
    ResourceCreateView,
    ResourceUpdateView,
    ResourceDeleteView,
)


urlpatterns = [
    path('', HubHomeView.as_view(), name='hub-home'),

    path('users/', UserListView.as_view(), name='list-user'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='update-user'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='delete-user'),

    path('projects/', ProjectListView.as_view(), name='list-project'),
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='update-project'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete-project'),

    path('resources/', ResourceListView.as_view(), name='list-resource'),
    path('resources/create/', ResourceCreateView.as_view(), name='create-resource'),
    path('resources/<int:pk>/update/', ResourceUpdateView.as_view(), name='update-resource'),
    path('resources/<int:pk>/delete/', ResourceDeleteView.as_view(), name='delete-resource'),
]