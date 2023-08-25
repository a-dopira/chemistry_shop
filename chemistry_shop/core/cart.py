from chemistry_shop import settings
from .models import Ingredient


class Cart(object):

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Ingredient.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = float(item['product'].price * item['quantity'])

            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, prod_id, quantity=1, update_quantity=False):
        prod_id = str(prod_id)

        if prod_id not in self.cart:
            self.cart[prod_id] = {'quantity': int(quantity), 'id': prod_id}

        if update_quantity:
            self.cart[prod_id]['quantity'] += int(quantity)

            if self.cart[prod_id]['quantity'] == 0:
                self.remove(prod_id)

        self.save()

    def remove(self, prod_id):
        if prod_id in self.cart:
            del self.cart[prod_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Ingredient.objects.get(pk=p)

        return float(sum(item['product'].price * item['quantity'] for item in self.cart.values()))

    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None