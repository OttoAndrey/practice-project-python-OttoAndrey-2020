from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from apps.test.models import Test
from apps.test.serializers import TestSerializer


class TestViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """
        list:
        Список всех объектов.

        create:
        Создаёт объект. Поле random_string рассчитывается автоматически.

        retrieve:
        Отображает только один объект.
        """

    serializer_class = TestSerializer
    queryset = Test.objects.all()
