from django.db import models

from location.models import Location


class User(models.Model):
    ROLES = [
        ('member', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    ]

    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    username = models.CharField(max_length=30, db_index=True, verbose_name='Логин', unique=True)
    password = models.CharField(max_length=50, verbose_name='Пароль')
    role = models.CharField(max_length=9, choices=ROLES, default="member", verbose_name='Роль')
    age = models.SmallIntegerField(verbose_name='Возраст')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Местоположение')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
