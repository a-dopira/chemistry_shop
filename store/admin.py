from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import F
from django.urls import reverse
from .models import Category, Ingredient, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "ingredient_count", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at"]

    def ingredient_count(self, obj):
        count = obj.ingredients.count()
        if count:
            url = (
                reverse("admin:store_ingredient_changelist")
                + f"?cat__id__exact={obj.id}"
            )
            return format_html('<a href="{}">{} ingredients</a>', url, count)
        return "0 ingredients"

    ingredient_count.short_description = "Ingredients"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "cat",
        "price",
        "quantity",
        "amount_with_unit",
        "unit",
        "is_published",
        "is_in_stock",
        "photo_preview",
    ]
    list_filter = ["is_published", "cat", "unit", "time_create"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = [
        "time_create",
        "time_update",
        "photo_preview",
        "amount_with_unit",
    ]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "content", "cat")}),
        ("Media", {"fields": ("photo", "photo_preview")}),
        (
            "Pricing & Stock",
            {
                "fields": ("price", "quantity", "unit", "amount", "amount_with_unit"),
                "description": "Set pricing, inventory and measurement information",
            },
        ),
        ("Status", {"fields": ("is_published",)}),
        (
            "Timestamps",
            {"fields": ("time_create", "time_update"), "classes": ("collapse",)},
        ),
    )

    actions = ["make_published", "make_unpublished"]

    def photo_preview(self, obj):
        if obj.photo and hasattr(obj.photo, "url"):
            try:
                return format_html(
                    '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover;" />',
                    obj.photo.url,
                )
            except ValueError:
                return "Photo file not found"
        return "No photo"

    photo_preview.short_description = "Photo Preview"

    def is_in_stock(self, obj):
        if obj.quantity > 0:
            return format_html(
                '<span style="color: green;">✓ In Stock ({})</span>', obj.quantity
            )
        return format_html('<span style="color: red;">✗ Out of Stock</span>')

    is_in_stock.short_description = "Stock Status"

    def amount_with_unit(self, obj):
        """Объединяет amount и unit в одном поле"""
        if obj.amount:
            return f"{obj.amount} {obj.unit}"
        return f"- {obj.unit}"

    amount_with_unit.short_description = "Amount with unit"
    amount_with_unit.admin_order_field = "amount"

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} ingredients published.")

    make_published.short_description = "Mark selected ingredients as published"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} ingredients unpublished.")

    make_unpublished.short_description = "Mark selected ingredients as unpublished"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["total_price"]

    def total_price(self, obj):
        if obj.id:
            return f"${obj.total_price}"
        return "-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "status",
        "total_amount",
        "is_paid",
        "created_at",
        "items_count",
    ]
    list_filter = ["status", "is_paid", "created_at", "country"]
    search_fields = ["first_name", "last_name", "email", "phone"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "total_amount_display",
        "payment_status",
        "order_summary",
    ]
    inlines = [OrderItemInline]

    fieldsets = (
        (
            "Customer Information",
            {"fields": ("first_name", "last_name", "email", "phone", "created_by")},
        ),
        ("Shipping Address", {"fields": ("address", "city", "zipcode", "country")}),
        (
            "Order Details",
            {"fields": ("status", "total_amount_display", "order_summary")},
        ),
        (
            "Payment Information",
            {
                "fields": (
                    "is_paid",
                    "paid_amount",
                    "payment_method",
                    "payment_intent",
                    "payment_status",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    actions = ["mark_as_paid", "mark_as_shipped", "mark_as_delivered"]

    def items_count(self, obj):
        count = obj.items.count()
        return f"{count} item{'s' if count != 1 else ''}"

    items_count.short_description = "Items"

    def total_amount_display(self, obj):
        return f"${obj.total_amount}"

    total_amount_display.short_description = "Total Amount"

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green;">✓ Paid</span>')
        return format_html('<span style="color: red;">✗ Unpaid</span>')

    payment_status.short_description = "Payment Status"

    def order_summary(self, obj):
        items = obj.items.all()
        summary = "<ul>"
        for item in items:
            summary += (
                f"<li>{item.quantity}x {item.product.title} - ${item.total_price}</li>"
            )
        summary += "</ul>"
        return mark_safe(summary)

    order_summary.short_description = "Order Summary"

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True, paid_amount=F("total_amount"))
        self.message_user(request, f"{queryset.count()} orders marked as paid.")

    mark_as_paid.short_description = "Mark selected orders as paid"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="shipped")
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")

    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")

    mark_as_delivered.short_description = "Mark selected orders as delivered"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price", "total_price"]
    list_filter = ["order__created_at", "product__cat"]
    search_fields = ["order__first_name", "order__last_name", "product__title"]
    readonly_fields = ["total_price"]


admin.site.site_header = "The Hag's Cure Admin"
admin.site.site_title = "The Hag's Cure"
admin.site.index_title = "Welcome to The Hag's Cure Administration"
