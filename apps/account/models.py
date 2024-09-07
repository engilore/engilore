from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from account.checkers import check_if_admin_or_guardian


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    subscribed = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    is_auxiliary = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    is_guardian = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    is_admin = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    ADMIN_EMAIL = 'lalo@engilore.com'


    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username
    
    def save(self, *args, **kwargs):
        check_if_admin_or_guardian(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
        ordering = ['date_joined']
