from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
from elservicecollection.models import Service
from elusermaneger.manager import ElUserManager


class ElBaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    login = models.CharField(max_length=255, verbose_name='Логин')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    loads_services = models.ManyToManyField(Service, verbose_name='Загруженные микросервисы', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ElUserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.email
