from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class SearchHistory(models.Model):
    time = models.DateTimeField(
        verbose_name='Время',
        auto_now_add=True
    )
    search_request = models.CharField(
        verbose_name='Поисковой запрос',
        max_length=300
    )

    def __str__(self):
        return {self.time: self.search_request}


class Status(models.Model):
    status = models.CharField(
        verbose_name='Статус пользователя',
        max_length=20
    )


class CustomUser(AbstractBaseUser):
    login = models.CharField(
        verbose_name='Логин',
        max_length=50,
    )
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
    search_history = models.ForeignKey(
        SearchHistory,
        on_delete=models.SET_NULL,
        verbose_name='История поиска',
        related_name='users',
        null=True
    )
    visit_history = models.DateTimeField(
        verbose_name='Время визита',
        auto_now_add=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=10,
        unique=True
    )

    class Meta:
        verbose_name = 'Пользoватель'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'phone_number'
