# Especificación de Diseño: Tienda de Videojuegos y Plataforma de Reseñas

Este documento describe la arquitectura, el esquema de base de datos, la lógica de negocio y las reglas de seguridad para el proyecto de la plataforma de videojuegos en Django.

---

## 1. Descripción General
La plataforma permite a los usuarios registrarse, explorar videojuegos, simular compras utilizando un sistema de saldo de usuario y escribir reseñas de los videojuegos que hayan adquirido. Además, cuenta con un sistema de restricción de contenidos por edad basado en la fecha de nacimiento del usuario y un panel de moderación para tareas administrativas.

---

## 2. Modelos de Base de Datos (6 Modelos)

### 2.1 `CustomUser` (en `users/models.py`)
Hereda de `AbstractUser` de Django para incluir campos para saldo, fecha de nacimiento y foto de perfil.
*   `username` (heredado)
*   `email` (unique=True, verbose_name="Correo Electrónico")
*   `password` (heredado)
*   `fecha_nacimiento` (DateField, null=False, blank=False)
*   `saldo` (DecimalField, max_digits=10, decimal_places=2, default=0.00)
*   `avatar` (ImageField, upload_to='avatars/', null=True, blank=True)
*   **Métodos**:
    *   `get_edad()`: Calcula la edad actual del usuario en base a `fecha_nacimiento` y la fecha de hoy.

### 2.2 `Desarrollador` (en `store/models.py`)
Representa a los estudios o empresas desarrolladoras de videojuegos.
*   `nombre` (CharField, max_length=100)
*   `sitio_web` (URLField, blank=True)
*   `pais` (CharField, max_length=50)

### 2.3 `Categoria` (en `store/models.py`)
Representa los géneros de los videojuegos (Acción, RPG, Deportes, etc.).
*   `nombre` (CharField, max_length=50, unique=True)
*   `descripcion` (TextField, blank=True)

### 2.4 `Videojuego` (en `store/models.py`)
Entidad principal del catálogo de la tienda.
*   `titulo` (CharField, max_length=150)
*   `descripcion` (TextField)
*   `precio` (DecimalField, max_digits=10, decimal_places=2)
*   `edad_minima` (IntegerField, default=0)
*   `imagen_portada` (ImageField, upload_to='portadas/')
*   `desarrollador` (ForeignKey a `Desarrollador`, on_delete=models.SET_NULL, null=True)
*   `categorias` (ManyToManyField a `Categoria`)

### 2.5 `Resena` (en `store/models.py`)
Opiniones y calificaciones de los usuarios sobre los juegos que compraron.
*   `usuario` (ForeignKey a `CustomUser`, on_delete=models.CASCADE)
*   `videojuego` (ForeignKey a `Videojuego`, on_delete=models.CASCADE)
*   `comentario` (TextField)
*   `calificacion` (IntegerField)  # Restringido entre 1 y 5
*   `fecha_creacion` (DateTimeField, auto_now_add=True)

### 2.6 `Compra` (en `store/models.py`)
Registra las transacciones y funciona como la biblioteca personal de videojuegos de cada usuario.
*   `usuario` (ForeignKey a `CustomUser`, on_delete=models.CASCADE)
*   `videojuego` (ForeignKey a `Videojuego`, on_delete=models.CASCADE)
*   `fecha_compra` (DateTimeField, auto_now_add=True)

---

## 3. Vistas y Lógica de Negocio

### 3.1 Catálogo y Restricción de Edad
*   **Vista del Catálogo (`store:index`)**: Muestra la lista de videojuegos.
    *   *Control de Edad*: Si el usuario está autenticado, se calcula su edad. Si `usuario.get_edad() < videojuego.edad_minima`, se desactivan los botones "Comprar" y "Ver Detalle" en el template, mostrando en su lugar un aviso de "Restringido (+X años)".
*   **Vista de Detalle (`store:videojuego_detalle`)**: Muestra la ficha técnica del juego y sus reseñas.
    *   *Control en Backend*: Si un usuario menor de edad intenta acceder directamente a la URL de detalle, la vista lo redirige al inicio con un mensaje de error utilizando `django.contrib.messages`.

### 3.2 Simulación de Compra y Carga de Saldo
*   **Cargar Saldo (`users:cargar_saldo`)**: Vista simple GET/POST.
    *   Presenta un formulario con un campo numérico. Al enviarse, suma el monto ingresado al campo `saldo` del `CustomUser` autenticado y guarda el modelo.
*   **Comprar Videojuego (`store:comprar_videojuego`)**: Ruta que procesa un POST.
    *   *Validaciones*:
        1.  Verificar que el usuario no posea ya el videojuego comprado (`Compra.objects.filter(...)`).
        2.  Verificar que el usuario cumpla con la edad mínima requerida por el juego.
        3.  Verificar saldo disponible: `usuario.saldo >= videojuego.precio`.
    *   *Ejecución*: Descuenta el precio del juego del saldo del usuario, guarda al usuario, crea el registro en `Compra` y redirige con un mensaje de éxito.
    *   *Fallo*: Redirige de vuelta al catálogo con una advertencia utilizando mensajes de Django.

### 3.3 Operaciones CRUD

#### CRUD 1: Videojuegos (Moderadores)
*   **Operaciones**: Crear, editar y eliminar videojuegos.
*   **Permisos**: Protegido utilizando el decorador `@permission_required` o el mixin de permisos correspondiente, buscando los permisos estándar de Django (`store.add_videojuego`, `store.change_videojuego`, `store.delete_videojuego`).
*   **Grupo**: Se creará un grupo en la base de datos llamado `Moderadores` que poseerá estos permisos específicos.

#### CRUD 2: Reseñas (Solo Propietarios)
*   **Operaciones**: Crear, editar y eliminar reseñas.
*   **Reglas**:
    *   Un usuario *solo* puede redactar una reseña si existe un registro de `Compra` que vincule a su usuario con ese videojuego.
    *   Un usuario *solo* puede editar o eliminar una reseña de la cual sea autor (`resena.usuario == request.user`).

---

## 4. Context Processor
Se creará un context processor personalizado `store.context_processors.categorias_context` que retorne todos los géneros cargados.
```python
def categorias_context(request):
    return {'global_categorias': Categoria.objects.all()}
```
Esto habilita a que cualquier template de la web pueda renderizar dinámicamente un listado de categorías en la barra de navegación.

---

## 5. Diseño y Estilos (Tailwind CSS)
*   Se usará Tailwind CSS (cargado mediante CDN en `base.html` en esta etapa de desarrollo).
*   Las vistas y los formularios usarán las clases de utilidad de Tailwind.
*   Se utilizará `django-widget-tweaks` para poder renderizar las clases de estilos dentro de los formularios sin alterar el backend en Python.
