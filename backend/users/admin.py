from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from foodgram import constants

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    empty_value_display = constants.EMPTY_VALUE_DISPLAY
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
