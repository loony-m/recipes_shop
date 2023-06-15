from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet
from tags.views import TagsViewSet
from recipes.views import IngredientsViewSet, RecipesViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
