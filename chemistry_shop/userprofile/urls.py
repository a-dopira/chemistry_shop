from django.urls import path

from userprofile.views import SignInPage, RegistrationPage, my_account, logout_user

urlpatterns = [
    path('login/', SignInPage.as_view(), name='login'),
    path('account/', my_account, name='user_account'),
    path('registration/', RegistrationPage.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]