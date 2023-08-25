from django.urls import path

from .views import *

urlpatterns = [
    path('', IngredientsList.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contacts, name='contact'),
    path('login/', SignInPage.as_view(), name='login'),
    path('account/', my_account, name='user_account'),
    path('registration/', RegistrationPage.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('category/<slug:cat_slug>/', CategoryList.as_view(), name='category'),
    path('product/<slug:prod_slug>/', SingleProduct.as_view(), name="single_product"),
    path('product/<int:prod_id>/add-to-cart', add_to_cart, name="add_to_cart"),
    path('cart/', cart_view, name="cart_view"),
    path('remove-from-cart/<str:prod_id>/', remove_from_cart, name="remove_from_cart"),
    path('change-quantity/<str:prod_id>/', change_quantity, name="change_quantity"),
    path('cart/checkout/', checkout, name="checkout"),
    path('search/', FormSearch.as_view(), name='search')
]