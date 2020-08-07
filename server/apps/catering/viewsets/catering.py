from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
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

    def list(self, request, *args, **kwargs):
        if 'caterings' in cache:
            results = cache.get('caterings')

        else:
            caterings = Catering.objects.all()
            serializer = CateringSerializer(caterings, many=True)
            results = serializer.data
            cache.set('caterings', results, timeout=900)

        return Response(results, status=status.HTTP_200_OK)
