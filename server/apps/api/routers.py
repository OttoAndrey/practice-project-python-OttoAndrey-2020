from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UsersViewSet


router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UsersViewSet, basename='users')
