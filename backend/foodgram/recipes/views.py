from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import (Ingredients, Recipes, Favorite, ShoppingCart,
                     IngredientsAmount)
from .serializers import (IngredientsSerializer, RecipesSerializator,
                          RecipeGeneralSerializer)
from .paginators import RecipesPaginator
from .permissions import OnlyAuthorOrRead, OnlyAdminOrRead
from .filters import IngredientsSearchFilter, AuthorAndTagFilter


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (OnlyAdminOrRead,)
    search_fields = ('^name',)
    filter_backends = (IngredientsSearchFilter,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializator
    pagination_class = RecipesPaginator
    filterset_class = AuthorAndTagFilter
    permission_classes = (OnlyAuthorOrRead,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_item(Favorite, user=request.user, recipe_id=pk)

        return self.delete_item(Favorite, user=request.user, recipe_id=pk)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_item(ShoppingCart, user=request.user, recipe_id=pk)

        return self.delete_item(ShoppingCart, user=request.user, recipe_id=pk)

    @action(detail=False, methods=['get'], permission_classes=[])
    def download_shopping_cart(self, request):

        ingredients_list = {}

        ingredients = IngredientsAmount.objects.filter(
            recipes__rn_cart__author=request.user).values_list(
            'amount', 'ingredient__name', 'ingredient__measurement_unit')

        for ingredient in ingredients:
            name = ingredient[1]

            if name in ingredients_list:
                ingredients_list[name]['amount'] += ingredient[0]
            else:
                ingredients_list[name] = {
                    'amount': ingredient[0],
                    'name': ingredient[1],
                    'measurement_unit': ingredient[2],
                }

        file_content = 'Список покупок: \n'
        for ingredient in ingredients_list.values():
            file_content += (f'- {ingredient["name"]}: '
                             f'{ingredient["amount"]} '
                             f'{ingredient["measurement_unit"]} \n')

        response = HttpResponse(file_content, 'Content-Type: text/plain')
        header = 'attachment; filename="recipe_ingredients.txt"'
        response['Content-Disposition'] = header

        return response

    def add_item(self, obj, user, recipe_id):
        if obj.objects.filter(author=user, recipes__id=recipe_id).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recipes = get_object_or_404(Recipes, id=recipe_id)

        obj.objects.create(
            author=user,
            recipes=recipes
        )

        serializer = RecipeGeneralSerializer(recipes)
        return Response(serializer.data)

    def delete_item(self, obj, user, recipe_id):
        item = obj.objects.filter(
            author=user,
            recipes__id=recipe_id
        )

        if item.exists():
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Рецепт отсутствует'},
            status=status.HTTP_400_BAD_REQUEST
        )
