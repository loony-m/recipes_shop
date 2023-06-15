from django.db import models
from django.contrib.auth import get_user_model

from tags.models import Tags
from .validators import validate_cooking_time

User = get_user_model()


class Ingredients(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipes(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингридиент',
        related_name='rn_recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовление',
        validators=[validate_cooking_time]
    )

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиентов в рецепте'
        verbose_name_plural = 'Количество ингридиентов в рецептах'

        constraints = [
            models.UniqueConstraint(
                fields=['recipes', 'ingredient'],
                name='Сочетание рецепта и ингридиента должно быть уникально!'
            )
        ]

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )


class Favorite(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='rn_favorite'
    )


class ShoppingCart(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='rn_cart'
    )
