from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager

class UserType(Enum):
    ADMIN = 1
    BANK_STAFF=2
    CUSTOMER = 3


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    last_name = models.CharField(null=False, max_length=80)
    first_name = models.CharField(null=False, max_length=80)
    user_type = models.SmallIntegerField(default=UserType.CUSTOMER.value, choices=[
                                         (ut.value, ut.name) for ut in UserType])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    def __str__(self):
        return self.email