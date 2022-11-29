from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True, verbose_name='Местоположение')
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    lng = models.DecimalField(max_digits=11, decimal_places=8)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
