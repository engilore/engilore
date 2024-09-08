from django.urls import path

from blog.views.post.view import (
    PostCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)

from blog.views.draft.view import (
    PostDraftListView,
    PostDraftDetailView,
    PostDraftUpdateView,
    PostDraftDeleteView
)


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:id>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:id>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('posts/drafts/', PostDraftListView.as_view(), name='post-draft-list'),
    path('posts/draft/<int:id>/', PostDraftDetailView.as_view(), name='post-draft-detail'),
    path('posts/drafts/<int:id>/edit/', PostDraftUpdateView.as_view(), name='post-draft-update'),
    path('posts/drafts/<int:id>/delete/', PostDraftDeleteView.as_view(), name='post-draft-delete'),
]