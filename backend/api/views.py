from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Ingredient, Category
from .serializers import (
    IngredientSerializer,
    IngredientListSerializer,
    CategorySerializer,
)
from .filters import IngredientFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("-time_create")
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            return queryset.select_related("cat")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return IngredientListSerializer
        return IngredientSerializer

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        category_slug = request.query_params.get("category")
        if not category_slug:
            return Response({"error": "Category slug required"}, status=400)

        ingredients = (
            self.get_queryset()
            .filter(cat__slug=category_slug, is_published=True)
            .select_related("cat")
        )

        serializer = self.get_serializer(ingredients, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def ingredients(self, request, slug=None):
        category = self.get_object()
        ingredients = Ingredient.objects.filter(
            cat=category, is_published=True
        ).select_related("cat")

        serializer = IngredientListSerializer(ingredients, many=True)
        return Response(
            {
                "category": CategorySerializer(category).data,
                "ingredients": serializer.data,
            }
        )
