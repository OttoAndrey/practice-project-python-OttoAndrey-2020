from rest_framework.viewsets import ModelViewSet

from apps.dish.models import Dish
from apps.dish.serializers import DishSerializer
from apps.main.permissions.dish import IsOwnerOrReadOnlyDishPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyDishPermission,)
