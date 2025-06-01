from django.urls import path

from store.cart.cart_view import (
    cart_view,
    checkout,
    change_quantity,
    add_to_cart,
    remove_from_cart,
)
from .views import *
from core.views import IngredientsList

urlpatterns = [
    path("cart/", cart_view, name="cart_view"),
    path("cart/checkout/", checkout, name="checkout"),
    path("category/<slug:cat_slug>/", IngredientsList.as_view(), name="category"),
    path("change-quantity/<str:prod_id>/", change_quantity, name="change_quantity"),
    path("product/<slug:prod_slug>/", SingleProduct.as_view(), name="single_product"),
    path("add-to-cart/<str:prod_id>/", add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<str:prod_id>/", remove_from_cart, name="remove_from_cart"),
    path("search/", FormSearch.as_view(), name="search_results"),
]
