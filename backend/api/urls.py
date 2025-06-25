from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, CategoryViewSet

router = DefaultRouter()
router.register("ingredients", IngredientViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
