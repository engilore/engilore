from django.urls import path

from account.views.register.view import RegisterView
from account.views.login.view import LoginView
from account.views.logout.view import LogoutView
from account.views.delete.view import DeleteUserView
from account.views.validate.view import ValidateUserView
from account.views.update.view import UpdateUserView

from account.views.guardians.view import GuardianListView

from account.views.manage.view import (
    UserListView, 
    UserDetailView, 
    UserUpdateView, 
    UserDeleteView, 
    UserRoleAssignView, 
    UserRoleRevokeView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteUserView.as_view(), name='delete'),
    path('validate/', ValidateUserView.as_view(), name='validate'),
    path('update/', UpdateUserView.as_view(), name='update'),

    path('guardians/', GuardianListView.as_view(), name='guardian-list'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:pk>/assign-role/', UserRoleAssignView.as_view(), name='user-assign-role'),
    path('users/<int:pk>/revoke-role/', UserRoleRevokeView.as_view(), name='user-revoke-role'),
]
