from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import waveapp.urls as wave_urls

urlpatterns = [
    path("", include(wave_urls)),
    path("accounts/", include("django.contrib.auth.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
