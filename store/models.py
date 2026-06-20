from django.db import models
from django.conf import settings

class Desarrollador(models.Model):
    nombre = models.CharField(max_length=100)
    sitio_web = models.URLField(blank=True)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    edad_minima = models.IntegerField(default=0)
    imagen_portada = models.ImageField(upload_to='portadas/')
    desarrollador = models.ForeignKey(Desarrollador, on_delete=models.SET_NULL, null=True)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.titulo

class Resena(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.videojuego.titulo}"

class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} compró {self.videojuego.titulo}"

