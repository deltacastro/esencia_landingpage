from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.page.views import main, aviso_privacidad
from apps.page.views import vLogin, vLogout

urlpatterns = [
    path('', main),
    path('aviso-privacidad', aviso_privacidad, name = 'aviso'),
    path('page/', include('apps.page.urls', namespace = 'page')),
    path('page/login/', vLogin, name = 'login'),
    path('page/logout/', vLogout, name = 'logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
