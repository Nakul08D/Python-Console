from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from base.models import BaseModel
from src.user.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = verbose_name_plural = _("Users")
        db_table = "user"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    @property
    def response_message(self) -> str:
        return f"{self.email}"

class UserCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_key_id = models.CharField(max_length=255)
    secret_access_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Credentials for {self.user.email}"