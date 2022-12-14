# Generated by Django 4.1.3 on 2022-11-17 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Фамилия')),
                ('username', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='Логин')),
                ('password', models.CharField(max_length=50, verbose_name='Пароль')),
                ('role', models.CharField(choices=[('member', 'Пользователь'), ('admin', 'Администратор'), ('moderator', 'Модератор')], default='member', max_length=9, verbose_name='Роль')),
                ('age', models.SmallIntegerField(verbose_name='Возраст')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location', verbose_name='Местоположение')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
