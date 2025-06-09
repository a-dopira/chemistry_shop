from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView


from .forms import RegisterUserForm, SignInForm, UserProfileForm
from store.models import Order

from userprofile.models import UserProfile


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

        try:
            profile = UserProfile.objects.select_related("user").get(
                user=self.request.user
            )
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=self.request.user)

        context.update(
            {
                "title": f"{self.request.user.username} | The Hag's Cure",
                "name": self.request.user.username,
                "email": self.request.user.email,
                "profile": profile,
            }
        )

        if self.request.htmx:
            current_page = int(self.request.GET.get("page", 1))
            context["total_shown"] = current_page * self.paginate_by
            context["total_items"] = self.get_queryset().count()
            context["target_container"] = "orders-container" 
        
        return context

    def get_template_names(self):
        if (
            self.request.headers.get("HX-Request")
            and self.request.GET.get("section") == "profile"
        ):
            return ["userprofile/profile_section_fragment.html"]
        elif self.request.headers.get("HX-Request"):
            load_more = self.request.GET.get("load_more")
            if load_more:
                return ["store/partials/load_more_response.html"]
            else:
                return ["userprofile/orders_fragment.html"]
        return [self.template_name]


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
        return reverse_lazy("showcase")

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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "userprofile/profile_update_modal.html"
    success_url = reverse_lazy("user_account")

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request"):
            return HttpResponse("", headers={"HX-Trigger": "profileUpdated"})
        return response

    def form_invalid(self, form):
        if self.request.headers.get("HX-Request"):
            return render(
                self.request, "userprofile/profile_form_fragment.html", {"form": form}
            )
        return super().form_invalid(form)

def logout_user(request):
    logout(request)
    return redirect("showcase")
