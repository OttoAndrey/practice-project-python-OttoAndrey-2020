from rest_framework.viewsets import ModelViewSet

from apps.dish.models import Dish
from apps.dish.serializers import DishSerializer
from apps.main.permissions.dish import IsOwnerOrReadOnlyDishPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class DishViewSet(ModelViewSet):
    """
    list:
    Список всех блюд.

    create:
    Создаёт объект блюда. Поля sum_of_calories и owner рассчитываются автоматически.
    Создавать блюда могут только авторизированные пользователи.

    retrieve:
    Отображает только одно созданное блюдо.

    update:
    Обновляет объект блюда. Обновить могут только владельцы блюда.

    partial_update:
    Обновляет объект блюда частично. Обновить могут только владельцы блюда.

    destroy:
    Удаляет объект блюда.
    Удалить могут только владельцы блюда.
    """

    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyDishPermission,)
