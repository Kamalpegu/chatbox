from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AuthUserProxy

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('displayname', 'image', 'info')}),
    ) + UserAdmin.fieldsets # type: ignore
    list_display = ('username', 'email', 'displayname')

@admin.register(AuthUserProxy)
class AuthUserProxyAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('displayname', 'image', 'info')}),
    ) + UserAdmin.fieldsets # type: ignore