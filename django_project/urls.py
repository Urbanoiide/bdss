from django.contrib import admin
from django.urls import path, include
from servicio_social.views import home 
from accounts.views import saludo_api
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("api/saludo/", saludo_api, name="saludo_api"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)