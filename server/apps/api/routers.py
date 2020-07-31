from rest_framework import routers

from apps.catering.viewsets import CateringViewSet
from apps.dish.viewsets.dish import DishViewSet
from apps.ingredient.viewsets.ingredient import IngredientViewSet
from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UsersViewSet

router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UsersViewSet, basename='users')
router.register('catering', CateringViewSet, basename='catering')
router.register('dish', DishViewSet, basename='dish')
router.register('ingredient', IngredientViewSet, basename='ingredient')
