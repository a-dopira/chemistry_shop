from django.urls import path
from .views import IngredientsList, SingleProduct, FormSearch

urlpatterns = [
    path("", IngredientsList.as_view(), name="showcase"),
    path("category/<slug:cat_slug>/", IngredientsList.as_view(), name="category"),
    path("product/<slug:prod_slug>/", SingleProduct.as_view(), name="single_product"),
    path("search/", FormSearch.as_view(), name="search_results"),
]
