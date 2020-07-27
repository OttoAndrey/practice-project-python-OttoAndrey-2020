from rest_framework.serializers import ModelSerializer

from apps.catering.models import Catering


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
                  'owner')
        extra_kwargs = {'avg_cost': {'read_only': True},
                        'longitude': {'read_only': True},
                        'latitude': {'read_only': True},
                        'owner': {'read_only': True},
                        }
