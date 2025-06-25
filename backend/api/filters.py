import django_filters as filters
from django.db.models import Q
from store.models import Ingredient, Category


class IngredientFilter(filters.FilterSet):

    cat = filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    category = filters.CharFilter(field_name="cat__slug", lookup_expr="exact")
    search = filters.CharFilter(method="search_filter")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = filters.BooleanFilter(method="stock_filter")
    ordering = filters.OrderingFilter(
        fields=("title", "price", "time_create", "quantity"),
        field_labels={
            "title": "Название",
            "price": "Цена",
            "time_create": "Дата создания",
            "quantity": "Количество",
        },
    )

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def stock_filter(self, queryset, name, value):
        if value:
            return queryset.filter(quantity__gt=0)
        return queryset.filter(quantity=0)

    class Meta:
        model = Ingredient
        fields = [
            "cat",
            "category",
            "is_published",
            "unit",
            "search",
            "min_price",
            "max_price",
            "in_stock",
            "ordering",
        ]
