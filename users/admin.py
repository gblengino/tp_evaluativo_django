from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'saldo', 'fecha_nacimiento', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'groups']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos de la tienda', {'fields': ('saldo', 'fecha_nacimiento', 'avatar')}),
    )