import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .cart import Cart
from store.models import Ingredient


def add_to_cart(request, prod_id):
    product = get_object_or_404(Ingredient, pk=prod_id)
    cart = Cart(request)

    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(prod_id, quantity, override_quantity=False)

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

