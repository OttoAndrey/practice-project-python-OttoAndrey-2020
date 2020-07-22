from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UsersSerializer


class UsersViewSet(mixins.CreateModelMixin,
                   GenericViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        return Response({
            'username': serializer.data['username'],
            'token': token.key,
        }, status=status.HTTP_201_CREATED, headers=headers)
