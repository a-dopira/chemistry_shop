from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls")),
    path("payment/", include("payment.urls")),
    path("", include("store.urls")),
    path("", include("userprofile.urls")),
    path("", include("core.urls")),
    path("api/", include("api.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
