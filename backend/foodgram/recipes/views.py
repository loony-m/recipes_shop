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

        carts = ShoppingCart.objects.filter(author=request.user).all()

        for cart in carts:
            for ingredient in cart.recipes.ingredients.all():
                id = ingredient.id

                ingredient_amount = IngredientsAmount.objects.get(
                    ingredient=id,
                    recipes=cart.recipes.id,
                ).amount

                if id in ingredients_list:
                    ingredients_list[id]['amount'] += ingredient_amount
                else:
                    ingredients_list[id] = {
                        'amount': ingredient_amount,
                        'name': ingredient.name,
                        'measurement_unit': ingredient.measurement_unit,
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
