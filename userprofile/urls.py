from django.urls import path

from userprofile.views import SignInPage, RegistrationPage, MyAccount, logout_user

urlpatterns = [
    path("login/", SignInPage.as_view(), name="login"),
    path("account/", MyAccount.as_view(), name="user_account"),
    path("registration/", RegistrationPage.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
]
