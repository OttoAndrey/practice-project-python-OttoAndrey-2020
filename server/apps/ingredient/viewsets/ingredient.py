from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from apps.ingredient.models import Ingredient
from apps.ingredient.serializers import IngredientSerializer


class IngredientViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    Список всех ингредиентов.

    create:
    Создаёт объект ингредиента. Создавать могут только авторизированные пользователи.

    retrieve:
    Отображает только один ингредиент.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
