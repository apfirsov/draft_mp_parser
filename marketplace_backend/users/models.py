from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    status = models.CharField(
        verbose_name='Статус пользователя',
        max_length=20
    )


class CustomUserManager(BaseUserManager):

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_number, password, **extra_fields)

    def get_by_natural_key(self, phone_number):
        return self.get(**{self.model.USERNAME_FIELD: phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=100
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True
    )
    visit_time = models.DateTimeField(
        verbose_name='Время визита',
        auto_now_add=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
        unique=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )

    class Meta:
        verbose_name = 'Пользoватель'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class SearchHistory(models.Model):
    time = models.DateTimeField(
        verbose_name='Время',
        auto_now_add=True
    )
    search_request = models.CharField(
        verbose_name='Поисковой запрос',
        max_length=300
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='serch_history',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return {self.time: self.search_request}
