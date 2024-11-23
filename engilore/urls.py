from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('', include('core.urls')),
    path('', include('argus.urls')),
    path('hub/', include('hub.urls')),
    path('account/', include('account.urls')),
    path('category/', include('category.urls')),
    path('blog/', include('blog.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)