from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('config/', admin.site.urls),
    path('admin/', include('core.urls.negocio_urls', namespace="admin"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
