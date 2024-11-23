from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('Email Address'),
        unique=True,
        max_length=255,
    )
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=50,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=50,
        null=False,
        blank=False
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=150,
        unique=True,
        null=False,
        blank=False
    )
    is_admin = models.BooleanField(
        verbose_name=_('Admin'),
        default=False,
        blank=False
    )
    is_engilorian = models.BooleanField(
        verbose_name=_('Engilorian'),
        default=False,
        blank=False
    )
    is_auxiliary = models.BooleanField(
        verbose_name=_('Auxiliary'),
        default=False,
        blank=False
    )
    is_verified = models.BooleanField(
        verbose_name=_('Verified'),
        default=False,
        blank=False
    )
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True,
    )

    def format_fields(self):
        if self.first_name:
            self.first_name = self.first_name.strip().capitalize()
        if self.last_name:
            self.last_name = self.last_name.strip().capitalize()
        if self.username:
            self.username = self.username.strip().lower()

    def check_and_set_admin_status(self):
        if self.email and self.email.endswith('@engilore.com'):
            self.is_admin = True
        else:
            self.is_admin = False

    def save(self, *args, **kwargs):
        self.format_fields()
        self.check_and_set_admin_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
