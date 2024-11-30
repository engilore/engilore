from django.conf import settings
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403, handler400
from django.conf.urls.static import static


urlpatterns = [
    path('', include('core.urls')),
    path('', include('argus.urls')),
    path('hub/', include('hub.urls')),
    path('account/', include('account.urls')),
    path('category/', include('category.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'core.views.view_404'
handler500 = 'core.views.view_500'
handler403 = 'core.views.view_403'
handler400 = 'core.views.view_400'