from django.urls import path

from userprofile.views import (
    SignInPage,
    RegistrationPage,
    MyAccount,
    UpdateProfileView,
    logout_user,
)

urlpatterns = [
    path("login/", SignInPage.as_view(), name="login"),
    path("account/", MyAccount.as_view(), name="user_account"),
    path("profile/update/", UpdateProfileView.as_view(), name="update_profile"),
    path("registration/", RegistrationPage.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
]
