from django.db.models import Avg
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.catering.models import Catering


@receiver(m2m_changed, sender=Catering.dishes.through)
def get_avg_cost(sender, action, instance, **kwargs):
    if action == 'post_add':
        instance.avg_cost = instance.dishes.all().aggregate(Avg('price'))['price__avg']
        instance.save()
