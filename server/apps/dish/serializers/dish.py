from rest_framework.serializers import ModelSerializer

from apps.dish.models import Dish


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name',
                  'photo',
                  'sum_of_calories',
                  'price',
                  'ingredients',)
        extra_kwargs = {'sum_of_calories': {'read_only': True}, }
