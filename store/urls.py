from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videojuegos/crear/', views.videojuego_crear, name='videojuego_crear'),
    path('videojuegos/<int:pk>/', views.videojuego_detalle, name='videojuego_detalle'),
    path('videojuegos/<int:pk>/comprar/', views.comprar_videojuego, name='comprar_videojuego'),
    path('videojuegos/<int:pk>/editar/', views.videojuego_editar, name='videojuego_editar'),
    path('videojuegos/<int:pk>/eliminar/', views.videojuego_eliminar, name='videojuego_eliminar'),
    path('videojuegos/<int:pk>/resenas/crear/', views.resena_crear, name='resena_crear'),
    path('resenas/<int:pk>/editar/', views.resena_editar, name='resena_editar'),
    path('resenas/<int:pk>/eliminar/', views.resena_eliminar, name='resena_eliminar'),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    path('historial/', views.historial_compras, name='historial_compras'),
]