from django.contrib import admin
from .models import Desarrollador, Categoria, Videojuego, Resena, Compra

@admin.register(Desarrollador)
class DesarrolladorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'sitio_web']
    search_fields = ['nombre', 'pais']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'precio', 'edad_minima', 'desarrollador']
    list_filter = ['categorias', 'desarrollador']
    search_fields = ['titulo']

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'videojuego', 'calificacion', 'fecha_creacion']
    list_filter = ['calificacion', 'fecha_creacion']
    search_fields = ['usuario__username', 'videojuego__titulo']

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'videojuego', 'fecha_compra']
    list_filter = ['fecha_compra']
    search_fields = ['usuario__username', 'videojuego__titulo']

