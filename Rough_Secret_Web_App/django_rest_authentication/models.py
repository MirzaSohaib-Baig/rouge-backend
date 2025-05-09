from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .utils import *


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractUser, PermissionsMixin):

    # Overrides Abstract User
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Additional Fields For Profile
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('trans', 'Transgender'), ('other', 'Other')]

    username = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True, default=None)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    zip_code = models.CharField(blank=True, null=True, max_length=50)
    city = models.CharField(blank=True, null=True, max_length=50)
    state = models.CharField(blank=True, null=True, max_length=50)
    country = models.CharField(blank=True, null=True, max_length=50)

    hidden_regions = models.JSONField(default=list)

    bio = models.TextField(max_length=500, blank=True, null=True)

    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)

    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions", blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.username}) - Verified: {self.is_verified}"

class GoogleCredentials(models.Model):

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='google_account')
    google_user_id = models.CharField(max_length=100, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()


class UserSettings(models.Model):

    is_payment_req = models.BooleanField(default=False)
    is_verification_req = models.BooleanField(default=False)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Settings For"