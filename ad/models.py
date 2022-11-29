from django.db import models

from category.models import Category
from user.models import User


class Ad(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Заголовок')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='user_ad')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Стоимость')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=True, verbose_name='Состояние')
    image = models.ImageField(upload_to='post_images/', null=True, blank=True, verbose_name='Изображение')
    category = models.ManyToManyField(Category, verbose_name='Категории')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name
