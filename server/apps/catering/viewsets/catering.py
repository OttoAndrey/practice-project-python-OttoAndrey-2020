from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.catering.models import Catering
from apps.catering.serializers import CateringSerializer
from apps.main.permissions import IsOwnerOrReadOnlyCateringPermission


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

    @method_decorator(cache_page(900))
    def list(self, request, *args, **kwargs):
        return super(CateringViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(900))
    def retrieve(self, request, *args, **kwargs):
        return super(CateringViewSet, self).retrieve(request, *args, **kwargs)
