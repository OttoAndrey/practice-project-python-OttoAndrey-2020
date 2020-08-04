from rest_framework.viewsets import ModelViewSet

from apps.catering.models import Catering
from apps.catering.serializers import CateringSerializer
from apps.main.permissions import IsOwnerOrReadOnlyCateringPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CateringViewSet(ModelViewSet):
    """
    list:
    Список всех заведений.

    create:
    Создаёт заведение.
    Поля latitude, longitude, owner только на чтение и рассчитываются автоматически при создании объекта.
    Создавать заведения могут только авторизированные пользователи.

    retrieve:
    Один объект заведения.

    update:
    Обновление объекта. Обновлять заведения могут только владельцы этого заведения.

    partial_update:
    Обновление некоторых полей объекта. Обновлять заведения могут только владельцы этого заведения.

    destroy:
    Удаление объекта. Удалить заведение может только владелец этого заведения.
    """

    serializer_class = CateringSerializer
    queryset = Catering.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyCateringPermission,)
