from django.urls import path

from category.views.category.view import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from category.views.topic.view import (
    TopicListView,
    TopicCreateView,
    TopicDetailView,
    TopicUpdateView,
    TopicDeleteView,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topic/create/', TopicCreateView.as_view(), name='topic-create'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:pk>/edit/', TopicUpdateView.as_view(), name='topic-update'),
    path('topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic-delete'),
]
