from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import OrderForm
from .models import Ingredient, Category, OrderItem
from .utils import DataMixin
from .cart import Cart


class SingleProduct(DataMixin, DetailView):
    model = Ingredient
    template_name = 'store/single_product.html'
    context_object_name = 'prod'
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=str(context['prod'].title) + ' | ' + str(context['prod'].cat.name),
            cat_selected=context['prod'].cat.id
        )
        return context | c_def


class CategoryList(DataMixin, ListView):
    paginate_by = 5
    template_name = 'core/home.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title=str(c.name) + ' | Categories',
            cat_selected=c.pk
        )
        return context | c_def

    def get_queryset(self):
        return Ingredient.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class FormSearch(ListView):
    model = Ingredient
    template_name = 'store/search_result.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('awesome_product', '')
        products = Ingredient.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('awesome_product', '')
        context['title'] = f"Search results for '{query}'"
        return context

# Cart itself


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