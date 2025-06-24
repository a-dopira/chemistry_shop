from django.urls import path
from .views import cart_view, change_quantity, add_to_cart, remove_from_cart

urlpatterns = [
    path("cart/", cart_view, name="cart_view"),
    path("change-quantity/<str:prod_id>/", change_quantity, name="change_quantity"),
    path("add-to-cart/<str:prod_id>/", add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<str:prod_id>/", remove_from_cart, name="remove_from_cart"),
]
