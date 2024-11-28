from django.urls import path

from category import views


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='list-category'),
    path('create/', views.CategoryCreateView.as_view(), name='create-category'),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view(), name='update-category'),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete-category'),

    path('topics/', views.TopicListView.as_view(), name='list-topic'),
    path('topics/create/', views.TopicCreateView.as_view(), name='create-topic'),
    path('topics/<int:pk>/update/', views.TopicUpdateView.as_view(), name='update-topic'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='delete-topic'),
]

