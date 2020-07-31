from rest_framework.viewsets import ModelViewSet

from apps.dish.models import Dish
from apps.dish.serializers import DishSerializer


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
