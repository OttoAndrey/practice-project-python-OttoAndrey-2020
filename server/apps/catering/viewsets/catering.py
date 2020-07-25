from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from yandex_geocoder import Client

from apps.catering.models import Catering
from apps.catering.serializers import CateringSerializer
from config.settings.local_settings import YD_GEO_API_KEY


class CateringViewSet(ModelViewSet):
    serializer_class = CateringSerializer
    queryset = Catering.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['avg_cost'] = 100.00 #TODO заглушка

        client = Client(YD_GEO_API_KEY)
        coordinates = client.coordinates(serializer.validated_data['address'])
        serializer.validated_data['longitude'] = coordinates[0]
        serializer.validated_data['latitude'] = coordinates[1]

        serializer.validated_data['owner'] = Token.objects.get(key=request.data['Authorization'][6:]).user

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)