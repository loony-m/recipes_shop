# Generated by Django 3.2.19 on 2023-06-21 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=15, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовление')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='rn_recipes', to='recipes.Ingredients', verbose_name='Ингридиент')),
                ('tags', models.ManyToManyField(to='tags.Tags', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rn_cart', to='recipes.recipes', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Список покупок',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientsAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredients', verbose_name='Ингридиент')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipes', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Количество ингридиентов в рецепте',
                'verbose_name_plural': 'Количество ингридиентов в рецептах',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rn_favorite', to='recipes.recipes', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'ordering': ['-id'],
            },
        ),
        migrations.AddConstraint(
            model_name='ingredientsamount',
            constraint=models.UniqueConstraint(fields=('recipes', 'ingredient'), name='Сочетание рецепта и ингридиента должно быть уникально!'),
        ),
    ]
