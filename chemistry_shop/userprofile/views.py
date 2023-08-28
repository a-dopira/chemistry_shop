from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from store.forms import RegisterUserForm, SignInForm
from store.utils import DataMixin


@login_required(login_url='login')
def my_account(request):
    return render(request, 'userprofile/user_profile.html', {'title': request.user.username})


def logout_user(request):
    logout(request)
    return redirect('home')


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