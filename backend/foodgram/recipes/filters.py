from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

from .models import Recipes

User = get_user_model()


class IngredientsSearchFilter(SearchFilter):
    search_param = 'name'


class AuthorAndTagFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(rn_favorite__author=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(rn_cart__author=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('tags', 'author')
