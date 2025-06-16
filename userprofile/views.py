
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from djoser import utils

from .activation import ActivationEmail, ConfirmationEmail
from store.models import Order
from .models import UserProfile
from .forms import RegisterUserForm, SignInForm, UserProfileForm

User = get_user_model()


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
                "email_verified": self.request.user.is_email_verified,
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
            return ["userprofile/partials/profile_section_fragment.html"]
        elif self.request.headers.get("HX-Request"):
            load_more = self.request.GET.get("load_more")
            if load_more:
                return ["store/partials/load_more_response.html"]
            else:
                return ["userprofile/partials/orders_fragment.html"]
        return [self.template_name]


class RegistrationPage(CreateView):
    form_class = RegisterUserForm
    template_name = "userprofile/register.html"
    success_url = reverse_lazy("registration_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration"
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        try:
            activation_email = ActivationEmail(self.request, {"user": user})
            activation_email.send([user.email])
        except Exception as e:
            raise Exception(f"Error sending activation email: {e}")

        if self.request.headers.get("HX-Request"):
            return HttpResponse(headers={"HX-Redirect": str(self.success_url)})
        return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "userprofile/partials/register_form_fragment.html",
                {"form": form, "title": "Registration"},
            )
        return super().form_invalid(form)


class RegistrationSuccessView(TemplateView):
    template_name = "userprofile/registration_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Завершение регистрации | The Hag's Cure"
        return context


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = "userprofile/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Authorization"
        return context

    def get_success_url(self):
        return reverse_lazy("user_account")

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_active:
            form.add_error(
                None,
                "Аккаунт не активирован. Проверьте email или "
                "запросите повторную отправку письма активации.",
            )
            return self.form_invalid(form)

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
                "userprofile/partials/login_form_fragment.html",
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
                self.request, "userprofile/partials/profile_form_fragment.html", {"form": form}
            )
        return super().form_invalid(form)


class ActivateUserView(TemplateView):
    def get(self, request, uid, token):
        try:
            user_id = utils.decode_uid(uid)
            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                    user.email_verified_at = timezone.now()
                    user.save()

                    confirmation_email = ConfirmationEmail(request, {"user": user})
                    confirmation_email.send([user.email])

                    messages.success(request, "Ваш аккаунт успешно активирован!")

                else:
                    messages.info(request, "Ваш аккаунт уже активирован.")
            else:
                messages.error(request, "Недействительная ссылка активации.")

        except (User.DoesNotExist, ValueError, TypeError) as e:
            raise Exception(f"Error activating user: {e}")

        return redirect("login")


class ResendActivationView(TemplateView):
    template_name = "userprofile/resend_activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Повторная отправка активации"
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    activation_email = ActivationEmail(request, {"user": user})
                    activation_email.send([user.email])
                    messages.success(request, "Письмо активации отправлено!")
                else:
                    messages.info(request, "Аккаунт уже активирован.")
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден.")

        if request.headers.get("HX-Request"):
            return render(
                request,
                "userprofile/resend_activation_form_fragment.html",
                {"email": email},
            )

        return render(
            request,
            self.template_name,
            {"title": "Повторная отправка активации", "email": email},
        )


def logout_user(request):
    request.session.flush()
    logout(request)
    return redirect("showcase")
