from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import CreateView, ListView

from .forms import RegisterUserForm, SignInForm
from store.models import Order


class MyAccount(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 3
    template_name = "userprofile/user_profile.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.filter(created_by=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": f"{self.request.user.username} | The Hag's Cure",
                "name": self.request.user.username,
                "email": self.request.user.email,
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            return render(self.request, "userprofile/orders_fragment.html", context)
        return super().render_to_response(context, **response_kwargs)


class RegistrationPage(CreateView):
    form_class = RegisterUserForm
    template_name = "userprofile/register.html"
    success_url = reverse_lazy("user_account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            response = HttpResponse()
            response["HX-Redirect"] = str(self.success_url)
            return response
        return response

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                "userprofile/register.html",
                {"form": form, "title": "Registration"},
            )
        return super().form_invalid(form)


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = "userprofile/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Authorization"
        return context

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = self.get_success_url()
            return response
        return response

    def form_invalid(self, form):
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "userprofile/login_form_fragment.html",
                {"form": form, "title": "Authorization"},
            )
        return super().form_invalid(form)


def logout_user(request):
    logout(request)
    return redirect("home")
