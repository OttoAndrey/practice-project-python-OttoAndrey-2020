from rest_framework.serializers import ModelSerializer
from yandex_geocoder import Client

from apps.catering.models import Catering
from config.settings.local_settings import YD_GEO_API_KEY


class CateringSerializer(ModelSerializer):
    class Meta:
        model = Catering
        fields = ('name',
                  'photo',
                  'open_time',
                  'close_time',
                  'address',
                  'avg_cost',
                  'longitude',
                  'latitude',
                  'dishes',
                  'owner')
        extra_kwargs = {'avg_cost': {'read_only': True},
                        'longitude': {'read_only': True},
                        'latitude': {'read_only': True},
                        'owner': {'read_only': True},
                        }

    def create(self, validated_data):
        client = Client(YD_GEO_API_KEY)
        coordinates = client.coordinates(validated_data['address'])
        validated_data['longitude'] = coordinates[0]
        validated_data['latitude'] = coordinates[1]

        validated_data['owner'] = self.context['request'].user

        catering = super().create(validated_data)

        return catering
