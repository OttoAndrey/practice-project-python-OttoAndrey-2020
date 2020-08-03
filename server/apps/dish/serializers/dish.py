from rest_framework.serializers import ModelSerializer

from apps.dish.models import Dish


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name',
                  'photo',
                  'sum_of_calories',
                  'price',
                  'ingredients',
                  'owner'
                  )
        extra_kwargs = {'sum_of_calories': {'read_only': True},
                        'owner': {'read_only': True}, }

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
