import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_htmx.http import HttpResponseClientRedirect

from .cart import Cart
from store.models import Ingredient, OrderItem
from store.forms import OrderForm


def add_to_cart(request, prod_id):
    product = get_object_or_404(Ingredient, pk=prod_id)
    cart = Cart(request)
    cart.add(prod_id)

    if request.htmx:
        response = HttpResponse(f"({len(cart)})")
        response["HX-Trigger"] = json.dumps({"cartUpdated": {"count": len(cart)}})
        return response

    messages.success(request, f"{product.title} added to cart!")
    return redirect("cart_view")


def remove_from_cart(request, prod_id):
    cart = Cart(request)
    cart.remove(prod_id)

    if request.htmx:
        response = render(request, "cart/cart_content.html", {"cart": cart})
        response["HX-Trigger"] = json.dumps({"cartUpdated": {"count": len(cart)}})
        return response

    return redirect("cart_view")


def change_quantity(request, prod_id):
    action = request.GET.get("action", "")
    cart = Cart(request)
    if action and action in ["increase", "decrease"]:
        quantity = 1 if action == "increase" else -1
        try:
            cart.add(prod_id, quantity, True)
        except Ingredient.DoesNotExist:
            cart.remove(prod_id)
    if request.htmx:
        if action == "get_count":
            return HttpResponse(f"({len(cart)})")
        else:
            response = render(request, "cart/cart_content.html", {"cart": cart})
            response["HX-Trigger"] = f"cartUpdated:{len(cart)}"
            return response
    return redirect("cart_view")


def cart_view(request):
    cart = Cart(request)

    removed_items = cart.clean_cart()

    if removed_items > 0:
        messages.warning(
            request,
            f"{removed_items} item(s) were removed from your cart because they are no longer available.",
        )

    return render(request, "cart/cart_view.html", {"title": "Cart", "cart": cart})


@login_required(login_url="login")
def checkout(request):
    cart = Cart(request)
    cart.clean_cart()

    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add some items before checkout.")
        return redirect("cart_view")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            if len(cart) == 0:
                messages.error(request, "Cannot create order with empty cart.")
                return redirect("cart_view")

            total_price = cart.get_total_cost()

            if total_price <= 0:
                messages.error(request, "Invalid order total. Please check your cart.")
                return redirect("cart_view")

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.total_amount = total_price
            order.save()

            order_items_created = 0
            for item in cart:
                product = item["product"]
                quantity = int(item["quantity"])

                if not product.is_in_stock or product.quantity < quantity:
                    messages.warning(
                        request,
                        f"Not enough {product.title} in stock. Available: {product.quantity}",
                    )
                    continue

                item_price = product.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item_price,
                    quantity=quantity,
                )

                product.quantity -= quantity
                product.save()

                order_items_created += 1

            if order_items_created == 0:
                order.delete()
                messages.error(
                    request, "Could not create order. All items are out of stock."
                )
                return redirect("cart_view")

            cart.clear()
            messages.success(
                request, f"Order #{order.id} has been created successfully!"
            )

            if request.htmx:
                return HttpResponseClientRedirect("user_account")

            return redirect("user_account")
    else:
        form = OrderForm()

    return render(
        request,
        "store/checkout.html",
        {
            "title": "Checkout",
            "cart": cart,
            "form": form,
        },
    )
