from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from store.forms import RegisterUserForm, SignInForm
from store.models import Order
from store.utils import DataMixin


class MyAccount(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 3
    template_name = 'userprofile/user_profile.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(created_by=user).prefetch_related('items')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()
        items = [order.items.filter(id=order.id).select_related('product') for order in orders]

        c_def = {
            'items': items,
            'title': self.request.user.username + "| The Hag's Cure",
            'name': self.request.user.username,
            'email': self.request.user.email,
        }

        return context | c_def


class RegistrationPage(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'userprofile/register.html'
    success_url = reverse_lazy('user_account')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return context | c_def


class SignInPage(DataMixin, LoginView):
    form_class = SignInForm
    template_name = 'userprofile/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('home')