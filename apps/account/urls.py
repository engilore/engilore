from django.urls import path

from account.views.register.view import RegisterView
from account.views.login.view import LoginView
from account.views.logout.view import LogoutView
from account.views.delete.view import DeleteUserView
from account.views.validate.view import ValidateUserView
from account.views.update.view import UpdateUserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteUserView.as_view(), name='delete'),
    path('validate/', ValidateUserView.as_view(), name='validate'),
    path('update/', UpdateUserView.as_view(), name='update'),
]
