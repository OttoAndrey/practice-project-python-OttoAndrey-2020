from django.contrib.auth.models import User
from django.db import models


class Catering(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название',
    )
    photo = models.ImageField(
        verbose_name='Фотография',
    )
    open_time = models.TimeField(
        verbose_name='Открытие',
    )
    close_time = models.TimeField(
        verbose_name='Закрытие',
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
    )
    avg_cost = models.FloatField(
        verbose_name='Средняя стоимость блюда',
        default=0.00
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name='Долгота',
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name='Широта',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведение'
        ordering = ['id']
