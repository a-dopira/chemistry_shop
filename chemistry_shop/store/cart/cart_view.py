from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from store.cart.cart import Cart
from store.forms import OrderForm
from store.models import OrderItem


def add_to_cart(request, prod_id):
    cart = Cart(request)
    cart.add(prod_id)

    return redirect('cart_view')


def remove_from_cart(request, prod_id):
    cart = Cart(request)
    cart.remove(str(prod_id))

    return redirect('cart_view')


def change_quantity(request, prod_id):
    action = request.GET.get('action', '')

    cart = Cart(request)
    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart.add(prod_id, quantity, True)

    return redirect('cart_view')


@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return redirect('user_account')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'title': 'Checkout',
        'cart': cart,
        'form': form,
    })


def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'title': 'Cart',
        'cart': cart
    })

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')