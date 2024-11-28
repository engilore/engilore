from django.urls import path

from account import views


urlpatterns = [
    path('manage/', views.AccountUpdateView.as_view(), name='account-manage'),
    path('delete/', views.AccountDeleteView.as_view(), name='account-delete'),
    path('<str:username>/', views.AccountProfileView.as_view(), name='account-profile'),
]
