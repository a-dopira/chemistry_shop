from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Ingredient(models.Model):

    UNIT_CHOICES = (
        ("kg", "kg"),
        ("g", "g"),
        ("l", "l"),
        ("ml", "ml"),
        ("piece", "piece"),
    )

    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    photo = models.ImageField(
        upload_to="ingredients/%Y/%m/",
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
    )
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default="piece",
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="ingredients",
        verbose_name="Category",
    )

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"prod_slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.quantity > 0

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["-time_create", "title"]
        indexes = [
            models.Index(fields=["is_published", "cat"]),
            models.Index(fields=["price"]),
        ]


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Ukraine")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    payment_intent = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    created_by = models.ForeignKey(
        User, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.zipcode}, {self.country}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_by", "created_at"]),
            models.Index(fields=["status"]),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Ingredient, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity}x {self.product.title}"

    @property
    def total_price(self):
        if self.price is not None:
            return self.price * self.quantity
        return 0

    def get_display_price(self):
        return self.price

    class Meta:
        unique_together = ["order", "product"]
