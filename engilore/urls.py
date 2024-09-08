from django.urls import path, include


urlpatterns = [
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
    path('category/', include('category.urls')),
]