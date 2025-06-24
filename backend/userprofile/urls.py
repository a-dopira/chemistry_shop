from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.SignInPage.as_view(), name="login"),
    path("account/", views.MyAccount.as_view(), name="user_account"),
    path("profile/update/", views.UpdateProfileView.as_view(), name="update_profile"),
    path("registration/", views.RegistrationPage.as_view(), name="register"),
    path("logout/", views.logout_user, name="logout"),
    path(
        "registration/success/",
        views.RegistrationSuccessView.as_view(),
        name="registration_success",
    ),
    path(
        "auth/activate/<str:uid>/<str:token>/",
        views.ActivateUserView.as_view(),
        name="activate_user",
    ),
    path(
        "resend-activation/",
        views.ResendActivationView.as_view(),
        name="resend_activation",
    ),
]
