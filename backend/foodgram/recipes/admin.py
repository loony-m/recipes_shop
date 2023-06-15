from .models import (Recipes, Ingredients, IngredientsAmount, Favorite,
                     ShoppingCart)
from django.contrib import admin


@admin.register(Recipes)
class AdminRecipes(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author'
    )

    list_filter = ('name', 'author', 'tags')


@admin.register(Ingredients)
class AdminIngredients(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )

    list_filter = ('name',)


@admin.register(IngredientsAmount)
class AdminIngredientsAmount(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipes',
        'ingredient',
        'amount'
    )


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'recipes'
    )


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'recipes'
    )
