from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.dish.models import Dish


@receiver(m2m_changed, sender=Dish.ingredients.through)
def get_sum_of_calories(sender, action, instance, **kwargs):
    if action == 'post_add':
        instance.sum_of_calories = instance.ingredients.all().aggregate(Sum('calorie'))['calorie__sum']
        instance.save()
