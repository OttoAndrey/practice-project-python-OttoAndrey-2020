from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    calorie = models.FloatField(
        verbose_name='Калорийность'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиент'
        ordering = ('id',)
