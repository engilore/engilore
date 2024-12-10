from django.urls import path

from blog.views.view import BlogHomeView

from blog.views.post.view import (
    BlogPostListView,
    BlogPostCreateView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

from blog.views.volume.view import (
    VolumeListView,
    VolumeCreateView,
    VolumeDetailView,
    VolumeUpdateView,
    VolumeDeleteView
)



urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog-home'),
    path('posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('create/', BlogPostCreateView.as_view(), name='create-blog-post'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='detail-blog-post'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='update-blog-post'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='delete-blog-post'),

    path('volumes/list/', VolumeListView.as_view(), name='list-volume'),
    path('volumes/create/', VolumeCreateView.as_view(), name='create-volume'),
    path('volumes/<slug:slug>/', VolumeDetailView.as_view(), name='detail-volume'),
    path('volumes/<slug:slug>/update/', VolumeUpdateView.as_view(), name='update-volume'),
    path('volumes/<slug:slug>/delete/', VolumeDeleteView.as_view(), name='delete-volume'),
]
