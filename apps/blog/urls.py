from django.urls import path

from blog.views.post.view import (
    PostCreateView,
    PostListView,
    UserPostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostTypeListView
)

from blog.views.draft.view import (
    PostDraftListView,
    PostDraftDetailView,
    PostDraftUpdateView,
    PostDraftDeleteView
)


urlpatterns = [
    path('post/types/', PostTypeListView.as_view(), name='post-types'),

    path('post/', PostListView.as_view(), name='post-list'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:id>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:id>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/user/', UserPostListView.as_view(), name='user-post-list'),

    path('post/draft/', PostDraftListView.as_view(), name='post-draft-list'),
    path('post/draft/<int:id>/', PostDraftDetailView.as_view(), name='post-draft-detail'),
    path('post/draft/<int:id>/edit/', PostDraftUpdateView.as_view(), name='post-draft-update'),
    path('post/draft/<int:id>/delete/', PostDraftDeleteView.as_view(), name='post-draft-delete'),
]