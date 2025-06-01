from chemistry_shop import settings
from decimal import Decimal
from store.models import Ingredient


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        items_to_remove = []

        for prod_id in list(self.cart.keys()):
            try:
                product = Ingredient.objects.get(pk=prod_id)
                item_data = self.cart[prod_id].copy()
                item_data["product"] = product
                item_data["total_price"] = float(product.price * item_data["quantity"])
                yield item_data
            except Ingredient.DoesNotExist:
                items_to_remove.append(prod_id)

        if items_to_remove:
            for prod_id in items_to_remove:
                del self.cart[prod_id]
            self.save()

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, override_quantity=False):
        """
        Добавляет товар в корзину или обновляет его количество
        """
        product_id = str(product_id)

        try:
            product = Ingredient.objects.get(id=product_id, is_published=True)
        except Ingredient.DoesNotExist:
            raise Ingredient.DoesNotExist("Product not found or not available")

        if not product.is_in_stock:
            raise ValueError("Product is out of stock")

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            new_quantity = self.cart[product_id]["quantity"] + quantity
        else:
            new_quantity = quantity

        if new_quantity > product.quantity:
            raise ValueError(
                f"Not enough items in stock. Available: {product.quantity}"
            )

        if new_quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id]["quantity"] = new_quantity

        self.save()

    def remove(self, prod_id):
        prod_id = str(prod_id)
        if prod_id in self.cart:
            del self.cart[prod_id]
            self.save()

    def clean_cart(self):
        """
        Удаляет из корзины товары, которых нет в наличии или которые не опубликованы
        Возвращает количество удаленных товаров
        """
        removed_items = 0
        items_to_remove = []

        for product_id, item in self.cart.items():
            try:
                product = Ingredient.objects.get(id=product_id, is_published=True)

                if not product.is_in_stock:
                    items_to_remove.append(product_id)
                    removed_items += 1
                    continue

                if item["quantity"] > product.quantity:
                    if product.quantity > 0:
                        self.cart[product_id]["quantity"] = product.quantity
                    else:
                        items_to_remove.append(product_id)
                        removed_items += 1

                if Decimal(item["price"]) != product.price:
                    self.cart[product_id]["price"] = str(product.price)

            except Ingredient.DoesNotExist:
                items_to_remove.append(product_id)
                removed_items += 1

        for product_id in items_to_remove:
            self.remove(product_id)

        return removed_items

    def is_empty(self):
        return len(self.cart) == 0

    def has_available_items(self):
        """Проверяет, есть ли в корзине доступные товары"""
        for product_id, item in self.cart.items():
            try:
                product = Ingredient.objects.get(id=product_id, is_published=True)
                if product.is_in_stock and product.quantity >= item["quantity"]:
                    return True
            except Ingredient.DoesNotExist:
                continue
        return False

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True

    def get_total_cost(self):
        total = 0
        items_to_remove = []

        for prod_id in self.cart.keys():
            try:
                product = Ingredient.objects.get(pk=prod_id)
                quantity = self.cart[prod_id]["quantity"]
                total += Decimal(product.price * quantity)
            except Ingredient.DoesNotExist:
                items_to_remove.append(prod_id)

        if items_to_remove:
            for prod_id in items_to_remove:
                del self.cart[prod_id]
            self.save()

        return total

    def get_item(self, product_id):
        prod_id = str(product_id)
        if prod_id in self.cart:
            return self.cart[prod_id]
        return None
