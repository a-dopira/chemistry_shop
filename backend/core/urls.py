from django.urls import path
from .views import about, contacts, serve_cached_image

urlpatterns = [
    path("about/", about, name="about"),
    path("contact/", contacts, name="contact"),
    path(
        "<str:model_name>_image/<str:cache_key>/",
        serve_cached_image,
        name="serve_cached_image",
    ),
]
