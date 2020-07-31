from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.ingredient.models import Ingredient
from apps.ingredient.serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
