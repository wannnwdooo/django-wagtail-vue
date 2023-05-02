from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=255,
        help_text=_('Required'),
        null=True,
        blank=True,
    )
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name='Электронная почта',
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]


