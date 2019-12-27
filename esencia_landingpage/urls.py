from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.page.views import main
from apps.page.views import vLogin, vLogout

urlpatterns = [
    path('', main),
    path('page/', include('apps.page.urls', namespace = 'page')),
    path('page/login/', vLogin, name = 'login'),
    path('page/logout/', vLogout, name = 'logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
