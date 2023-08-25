from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import SignInForm, OrderForm, RegisterUserForm
from .models import *
from .utils import *
from .cart import Cart


class IngredientsList(DataMixin, ListView):

    paginate_by = 6
    model = Ingredient
    template_name = 'core/index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='The Hag\'s Cure')
        return context | c_def


def about(request):
    context = {
        'title': 'Information page'
    }
    return render(request, 'core/about.html', context=context)


class SingleProduct(DataMixin, DetailView):
    model = Ingredient
    template_name = 'core/single_product.html'
    context_object_name = 'prod'
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=str(context['prod'].title) + ' | ' + str(context['prod'].cat.name),
            cat_selected=context['prod'].cat.id
        )
        return context | c_def

@login_required(login_url='login')
def my_account(request):
    return render(request, 'core/user_profile.html', {'title': request.user.username})

def contacts(request):
    context = {
        'title': 'Contacts',
        'social_media': [
            ('instagram', 'https://www.instagram.com/dizainmebli/'),
            ('facebook', 'https://www.facebook.com/a.dopira.u/'),
            ('github', 'https://github.com/a-dopira'),
            ('linkedIn', 'https://www.linkedin.com/in/anton-dopira-15b8b9210/')
        ]
    }
    return render(request, 'core/contacts.html', context=context)


def sign_in(request):
    context = {
        'title': 'Information page'
    }
    return render(request, 'core/sign_in.html', context=context)


class CategoryList(DataMixin, ListView):
    paginate_by = 5
    model = Ingredient
    template_name = 'core/index.html'
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

class RegistrationPage(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('user_account')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return context | c_def


class SignInPage(DataMixin, LoginView):
    form_class = SignInForm
    template_name = 'core/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


class FormSearch(ListView):
    model = Ingredient
    template_name = 'core/search_result.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('single_product', '')
        products = Ingredient.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return products


def logout_user(request):
    logout(request)
    return redirect('home')

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

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return redirect('user_account')
    else:
        form = OrderForm()

    return render(request, 'core/checkout.html', {
        'title': 'Checkout',
        'cart': cart,
        'form': form,
    })

def cart_view(request):
    cart = Cart(request)

    return render(request, 'core/cart_view.html', {
        'title': 'Cart',
        'cart': cart
    })

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found, motherfucker</h1>')