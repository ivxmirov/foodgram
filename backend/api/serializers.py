import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram import constants
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from users.models import Follow

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)


class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(
        max_length=constants.PASSWORD_MAX_LENGTH,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
        )


class CustomUserSerializer(UserSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'avatar',
            'email',
            'first_name',
            'id',
            'is_subscribed',
            'last_name',
            'username'
        )
        read_only_fields = ('id', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.follower.filter(author=obj).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.ReadOnlyField(source='recipe.id')
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class FollowSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, source='author.avatar')
    email = serializers.ReadOnlyField(source='author.email')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    id = serializers.ReadOnlyField(source='author.id')
    is_subscribed = serializers.SerializerMethodField()
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(default=0)
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Follow
        fields = (
            'avatar',
            'email',
            'first_name',
            'id',
            'is_subscribed',
            'last_name',
            'recipes_count',
            'recipes',
            'username'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Follow.objects.filter(author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = int(request.GET.get('recipes_limit', constants.PAGE_SIZE))
        return ShortRecipeSerializer(
            Recipe.objects.filter(author=obj.author)[:limit],
            many=True,
            context={'request': request},
        ).data

    # def get_recipes_count(self, obj):
    #     return Recipe.objects.filter(author=obj.author).count()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'amount',
            'id',
            'measurement_unit',
            'name'
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        label='Tags',
    )
    ingredients = RecipeIngredientCreateSerializer(
        many=True,
        label='Ingredients',
    )
    image = Base64ImageField(
        allow_null=True,
        label='images'
    )

    class Meta:
        model = Recipe
        fields = (
            'cooking_time',
            'image',
            'ingredients',
            'name',
            'tags',
            'text',
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def create_ingredients(self, ingredients, recipe):
        result = []
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
            amount = ingredient_data['amount']
            recipe_ingredient = RecipeIngredient(
                ingredient=ingredient, recipe=recipe, amount=amount
            )
            result.append(recipe_ingredient)
        RecipeIngredient.objects.bulk_create(result)

    def create_tags(self, tags, recipe):
        recipe.tags.set(tags)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        return super().update(instance, validated_data)

    def validate(self, data):

        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Добавьте хотя бы один ингредиент !'})
        ingredients_ids = [ingredient['id'] for ingredient in ingredients]
        existing_ingredients = Ingredient.objects.filter(
            id__in=ingredients_ids)
        if existing_ingredients.count() != len(ingredients_ids):
            missing_ids = set(ingredients_ids) - set(
                existing_ingredients.values_list('id', flat=True)
            )
            raise serializers.ValidationError(
                f'Ингредиент с id: {missing_ids} не существует !'
            )
        data['ingredients'] = ingredients

        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Добавьте хотя бы один тег !'})
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги не должны повторяться !')
        data['tags'] = tags

        return data


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    ingredients = RecipeIngredientReadSerializer(
        source='ingredient_list',
        many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'cooking_time',
            'id',
            'image',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'tags',
            'text',
        )

    def check_user_status(self, obj, model_class):
        user = self.context.get('request')
        return (
            user
            and user.user.is_authenticated
            and model_class.objects.filter(recipe=obj,
                                           user=user.user).exists()
        )

    def get_is_favorited(self, obj):
        return self.check_user_status(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.check_user_status(obj, ShoppingList)


class ShoppingListSerializer(FavoriteSerializer):

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
