from rest_framework.viewsets import ModelViewSet

from apps.catering.models import Catering
from apps.catering.serializers import CateringSerializer


class CateringViewSet(ModelViewSet):
    serializer_class = CateringSerializer
    queryset = Catering.objects.all()
