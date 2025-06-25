from rest_framework import serializers
from store.models import Category, Ingredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    cat = CategorySerializer(read_only=True)
    cat_id = serializers.IntegerField(write_only=True)

    thumbnail_mini = serializers.ReadOnlyField()
    thumbnail_small = serializers.ReadOnlyField()
    thumbnail_large = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "photo",
            "price",
            "quantity",
            "unit",
            "amount",
            "time_create",
            "time_update",
            "is_published",
            "cat",
            "cat_id",
            "thumbnail_mini",
            "thumbnail_small",
            "thumbnail_large",
            "is_in_stock",
        ]
        read_only_fields = ["slug", "time_create", "time_update"]


class IngredientListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source="cat", read_only=True)
    thumbnail_small = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "quantity",
            "unit",
            "thumbnail_small",
            "is_published",
            "category",
            "is_in_stock",
        ]
