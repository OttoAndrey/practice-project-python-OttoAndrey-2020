from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UsersViewSet
from apps.catering.viewsets import CateringViewSet


router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UsersViewSet, basename='users')
router.register('catering', CateringViewSet, basename='catering')
