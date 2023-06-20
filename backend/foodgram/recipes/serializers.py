from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (Ingredients, IngredientsAmount, Recipes, Favorite,
                     ShoppingCart)
from tags.serializers import TagsSerializer
from api.serializers import UserSerializer


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAmountSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        ingredient = IngredientsAmount.objects.get(
            ingredient=obj.pk,
            recipes=obj.rn_recipes.first().id
        )
        return ingredient.amount


class RecipesSerializator(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagsSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientsAmountSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(recipes=obj.pk, author=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipes=obj.pk,
                                           author=user).exists()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipes.objects.create(image=image, **validated_data)
        recipe.tags.set(self.initial_data.get('tags'))

        ingredients_id = self.add_ingredients(
            ingredients,
            recipe
        )
        recipe.ingredients.set(ingredients_id)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        tags = self.initial_data.get('tags')
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        ingredients = self.initial_data.get('ingredients')
        if ingredients:
            IngredientsAmount.objects.filter(recipes=instance).delete()
            ingredients_id = self.add_ingredients(ingredients, instance)
            instance.ingredients.set(ingredients_id)

        instance.save()
        return instance

    def add_ingredients(self, ingredients, recipe):
        ingredients_id = []

        for ingredient in ingredients:
            ingredient_item = Ingredients.objects.filter(
                pk=ingredient.get('id')
            )
            # todo: ингридиенты все нужные. Здесь мы проверям каждый,
            # который передает пользователь в api
            # если выносить проверку в другое место получится то же самое
            if ingredient_item.exists():
                IngredientsAmount.objects.create(
                    recipes=recipe,
                    ingredient=ingredient_item.first(),
                    amount=ingredient.get('amount')
                )
                ingredients_id.append(ingredient.get('id'))

        return ingredients_id

        # todo: bulk_create не возвращает id обьектов,
        # а мне они нужны дальше по коду

        # ingredient_list = []
        # ingredients_id = []

        # for ingredient in ingredients:
        #     ingredient_list.append(
        #         IngredientsAmount(
        #             recipes=recipe,
        #             ingredient=Ingredients.objects.filter(pk=ingredient.get('id')).first(),
        #             amount=ingredient.get('amount')
        #         )
        #     )
        # objects = IngredientsAmount.objects.bulk_create(ingredient_list)

        # for objects in objects:
        #     ingredients_id.append(objects.id)

        # return ingredients_id


class RecipeGeneralSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
