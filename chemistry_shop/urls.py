from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from chemistry_shop import settings
from store.views import page_not_found
from core.views import IngredientsList, about, contacts

urlpatterns = [
    path("about/", about, name="about"),
    path("admin/", admin.site.urls),
    path("contact/", contacts, name="contact"),
    path("", IngredientsList.as_view(), name="home"),
    path("", include("store.urls")),
    path("", include("userprofile.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
