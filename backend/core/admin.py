from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_verified', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'user_type', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'is_verified', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
