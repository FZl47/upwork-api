from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ClientUser, FreelancerUser, SuperUser, BaseUser

admin.site.register(BaseUser)


@admin.register(ClientUser)
class ClientUserAdmin(UserAdmin):
    model = ClientUser
    list_display = ('role', 'id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    readonly_fields = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Role info', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'first_name', 'last_name', 'email'),
        }),
    )


@admin.register(FreelancerUser)
class FreelancerUserAdmin(UserAdmin):
    model = FreelancerUser
    list_display = ('role', 'id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    readonly_fields = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Role info', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'first_name', 'last_name', 'email'),
        }),
    )


@admin.register(SuperUser)
class SuperUserAdmin(UserAdmin):
    model = SuperUser
    list_display = ('role', 'id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    readonly_fields = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Role info', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'first_name', 'last_name', 'email'),
        }),
    )
