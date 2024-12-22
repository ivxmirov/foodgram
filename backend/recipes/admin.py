from django.contrib import admin
from django.contrib.auth import get_user_model
from admin_auto_filters.filters import AutocompleteFilter

from foodgram import constants
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)

User = get_user_model()


class AuthorFilter(AutocompleteFilter):
    title = 'Автор рецепта'
    field_name = 'author'


class IngredientFilter(AutocompleteFilter):
    title = 'Ингредиент'
    field_name = 'ingredients'


class RecipeFilter(AutocompleteFilter):
    title = 'Рецепт'
    field_name = 'recipe'


class TagFilter(AutocompleteFilter):
    title = 'Тег'
    field_name = 'tags'


class UserFilter(AutocompleteFilter):
    title = 'Пользователь'
    field_name = 'user'


class RecipeIngredientInLine(admin.TabularInline):
    autocomplete_fields = ('ingredient',)
    extra = constants.INLINE_EXTRA
    model = RecipeIngredient

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'recipe', 'ingredient')
        return queryset


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    list_display = ('user', 'recipe')
    list_filter = (UserFilter, RecipeFilter)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'user', 'recipe')
        return queryset


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    filter_horizontal = ('tags',)
    inlines = (RecipeIngredientInLine,)
    list_display = ('name', 'author', 'get_favorite_count')
    list_filter = (AuthorFilter, IngredientFilter, TagFilter)
    search_fields = ('name',)

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite.count()

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request)
            .select_related('author')
            .prefetch_related('ingredients', 'tags')
        )
        return queryset


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    list_display = ('user', 'recipe')
    list_filter = (UserFilter, RecipeFilter)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'user', 'recipe')
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)
