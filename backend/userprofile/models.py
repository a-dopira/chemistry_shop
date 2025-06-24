from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.get_filename import get_filename
from core.mixins import ImageCacheMixin


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def is_email_verified(self):
        return self.email_verified_at is not None


class UserProfile(ImageCacheMixin, models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    userphoto = models.ImageField(
        upload_to=get_filename,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def avatar_mini(self):
        return self.get_cached_image_url("userphoto", "mini")

    @property
    def avatar_small(self):
        return self.get_cached_image_url("userphoto", "small")

    @property
    def is_profile_filled(self):
        return bool(self.address and self.phone_number)

    def save(self, *args, **kwargs):
        photo_changed = False
        if self.pk:
            old_instance = UserProfile.objects.get(pk=self.pk)
            if old_instance.userphoto != self.userphoto:
                photo_changed = True

        super().save(*args, **kwargs)

        if photo_changed:
            self.invalidate_image_cache()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users' Profiles"

    def __str__(self):
        return f"User's Profile: {self.user.username}"
