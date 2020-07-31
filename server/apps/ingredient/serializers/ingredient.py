from rest_framework.serializers import ModelSerializer

from apps.ingredient.models import Ingredient


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',
                  'calorie',)
