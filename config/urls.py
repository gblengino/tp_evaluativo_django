from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from users.views import register_user, cargar_saldo, mi_perfil

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_user, name='register'),
    path('accounts/cargar-saldo/', cargar_saldo, name='cargar_saldo'),
    path('accounts/profile', mi_perfil, name='mi_perfil')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)