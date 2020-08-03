from rest_framework.viewsets import ModelViewSet

from apps.catering.models import Catering
from apps.catering.serializers import CateringSerializer
from apps.main.permissions import IsOwnerOrReadOnlyCateringPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CateringViewSet(ModelViewSet):
    serializer_class = CateringSerializer
    queryset = Catering.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyCateringPermission,)
