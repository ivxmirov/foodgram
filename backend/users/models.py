from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from foodgram import constants


class Follow(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='check_follower_author',
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class User(AbstractUser):
    avatar = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Фото профиля',
        upload_to='media/users_avatars/'
    )
    email = models.EmailField(
        max_length=constants.EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=constants.FIRST_NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=constants.LAST_NAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    username = models.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Никнейм содержит запрещенные символы! Пожалуйста, '
                    'используйте только буквы, цифры и символы .@+-'
        ), ],
        verbose_name='Никнейм'
    )

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'password',
        'username'
    ]
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
