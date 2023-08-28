from django.urls import path

from .views import *

urlpatterns = [
    path('cart/', cart_view, name="cart_view"),
    path('cart/checkout/', checkout, name="checkout"),
    path('category/<slug:cat_slug>/', CategoryList.as_view(), name='category'),
    path('change-quantity/<str:prod_id>/', change_quantity, name="change_quantity"),
    path('product/<slug:prod_slug>/', SingleProduct.as_view(), name="single_product"),
    path('product/<int:prod_id>/add-to-cart', add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<str:prod_id>/', remove_from_cart, name="remove_from_cart"),
    path('search/', FormSearch.as_view(), name='search')
]