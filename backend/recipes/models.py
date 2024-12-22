from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram import constants

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'),
        )

    def __str__(self):
        return (f'Рецепт "{self.recipe}" в избранном у пользователя '
                f'"{self.user}"')


class Ingredient(models.Model):
    name = models.CharField(
        max_length=constants.INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=constants.MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=constants.RECIPE_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Список ингредиентов'
    )
    text = models.CharField(
        max_length=constants.RECIPE_TEXT_MAX_LENGTH,
        verbose_name='Порядок приготовления'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                constants.COOKING_TIME_MIN,
                message=(f'Минимальное время приготовления - '
                         f'{constants.COOKING_TIME_MIN} мин. !')
            ),
            MaxValueValidator(
                constants.COOKING_TIME_MAX,
                message=(f'Максимальное время приготовления - '
                         f'{constants.COOKING_TIME_MAX} мин. !')
            ),
        ],
        verbose_name='Время приготовления (в минутах)'
    )
    image = models.ImageField(
        verbose_name='Изображение готового блюда',
        upload_to='media/recipes_images/'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.RESTRICT,
        related_name='ingredient',
        verbose_name='ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                constants.INGREDIENT_AMOUNT_MIN,
                message=(f'Минимальное количество - '
                         f'{constants.INGREDIENT_AMOUNT_MIN} !')
            ),
            MaxValueValidator(
                constants.INGREDIENT_AMOUNT_MAX,
                message=(f'Максимальное количество - '
                         f'{constants.INGREDIENT_AMOUNT_MAX} !')
            ),
        ],
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_in_recipe',
            ),
        )

    def __str__(self):
        return (f'Рецепт "{self.recipe}" содержит ингредиент '
                f'"{self.ingredient}"')


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_shopping_list'
            ),
        )

    def __str__(self):
        return (f'Рецепт "{self.recipe}" в списке покупок '
                f'у пользователя "{self.user}"')


class Tag(models.Model):
    name = models.CharField(
        max_length=constants.TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.CharField(
        max_length=constants.TAG_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Короткая ссылка'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
