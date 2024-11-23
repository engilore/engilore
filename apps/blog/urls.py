from django.urls import path

from blog import views


urlpatterns = [
    path('', views.BlogHomeView.as_view(), name='blog-home'),
    path('posts/', views.BlogPostListView.as_view(), name='list-blog-posts'),
    path('create/', views.BlogPostCreateView.as_view(), name='create-blog-post'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='detail-blog-post'),
    path('<slug:slug>/update/', views.BlogPostUpdateView.as_view(), name='update-blog-post'),
    path('<slug:slug>/delete/', views.BlogPostDeleteView.as_view(), name='delete-blog-post'),
]
