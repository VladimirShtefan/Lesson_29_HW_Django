from django.db import models
from rest_framework import serializers

from location.models import Location, LocationPostSerializer


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


class UserSerializer(serializers.ModelSerializer):
    total_ads = serializers.SerializerMethodField()

    def get_total_ads(self, obj):
        return obj.user_ad.filter(is_published=True).count()

    class Meta:
        model = User
        depth = 1
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = LocationPostSerializer()

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        return User.objects.create(location=location, **validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'location')
