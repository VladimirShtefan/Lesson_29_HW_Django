from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import smart_str
from rest_framework import serializers

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


class AdListSerializer(serializers.ModelSerializer):
    queryset = Ad.objects.all().select_related('author').select_related('author__location').prefetch_related('category')

    class Meta:
        model = Ad
        depth = 2
        fields = '__all__'


class CreatableSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            print(type(data))
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class AdPostSerializer(serializers.ModelSerializer):
    category = CreatableSlugRelatedField(
        queryset=Category.objects.all(),
        many=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ad
        fields = ('id', 'name', 'author', 'price', 'description', 'is_published', 'image', 'category')


class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)


class AdPatchSerializer(PatchModelSerializer):
    category = CreatableSlugRelatedField(
        queryset=Category.objects.all(),
        many=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ad
        fields = '__all__'
