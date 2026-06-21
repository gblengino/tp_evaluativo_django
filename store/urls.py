from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videojuegos/crear/', views.videojuego_crear, name='videojuego_crear'),
    path('videojuegos/<int:pk>/', views.videojuego_detalle, name='videojuego_detalle'),
    path('videojuegos/<int:pk>/comprar/', views.comprar_videojuego, name='comprar_videojuego'),
]