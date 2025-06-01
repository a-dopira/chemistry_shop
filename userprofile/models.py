from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.get_filename import get_filename


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def profile(self):
        return UserProfile.objects.get(user=self)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    userphoto = models.ImageField(upload_to=get_filename)

    def __str__(self):
        return self.user.username
