from django.db import models

from apps.ingredient.models import Ingredient


class Dish(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    photo = models.ImageField(
        verbose_name='Фотография',
    )
    sum_of_calories = models.FloatField(
        verbose_name='Сумма калорий',
        null=True,
        default=0.00,
    )
    price = models.IntegerField(
        verbose_name='Стоимость',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
    )

    def __str__(self):
        return self.name