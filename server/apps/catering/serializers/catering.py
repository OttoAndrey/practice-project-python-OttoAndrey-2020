from rest_framework.serializers import ModelSerializer

from apps.catering.models import Catering


class CateringSerializer(ModelSerializer):
    class Meta:
        model = Catering
        fields = '__all__'
        extra_kwargs = {'avg_cost': {'read_only': True},
                        'longitude': {'read_only': True},
                        'latitude': {'read_only': True},
                        'owner': {'read_only': True},
                        }
