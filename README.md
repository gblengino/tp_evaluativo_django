# GameStore 🎮

Plataforma de compra y reseña de videojuegos desarrollada con Django. Trabajo Práctico Evaluativo — Ingeniería de Software 2026.

---

## Descripción

GameStore es una tienda online de videojuegos que permite a los usuarios registrarse, explorar un catálogo, simular compras usando un sistema de saldo virtual y escribir reseñas de los juegos que hayan adquirido. Incluye un sistema de restricción de contenidos por edad y un panel de moderación para la gestión del catálogo.

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje base |
| Django 6.0.6 | Framework web |
| SQLite3 | Base de datos |
| Tailwind CSS (CDN) | Estilos |
| django-widget-tweaks | Renderizado de formularios |
| Pillow | Manejo de imágenes |

---

## Modelos de base de datos

El proyecto cuenta con **6 modelos** relacionados entre sí:

### `CustomUser` — `users/models.py`
Extiende `AbstractUser` de Django con campos adicionales para la tienda.
- `email` — único y obligatorio
- `fecha_nacimiento` — usado para calcular la edad y aplicar restricciones de contenido
- `saldo` — saldo virtual para simular compras (`DecimalField`)
- `avatar` — foto de perfil (`ImageField`)
- `get_edad()` — método que calcula la edad actual a partir de `fecha_nacimiento`

### `Desarrollador` — `store/models.py`
Representa los estudios o empresas creadoras de videojuegos.
- `nombre`, `pais`, `sitio_web`

### `Categoria` — `store/models.py`
Géneros de videojuegos (Acción, RPG, Deportes, etc.).
- `nombre` (único), `descripcion`

### `Videojuego` — `store/models.py`
Entidad principal del catálogo.
- `titulo`, `descripcion`, `precio`, `edad_minima`
- `imagen_portada` — `ImageField`, subida a `media/portadas/`
- `desarrollador` — `ForeignKey` a `Desarrollador`
- `categorias` — `ManyToManyField` a `Categoria`

### `Resena` — `store/models.py`
Opiniones de usuarios sobre juegos que compraron.
- `usuario` — `ForeignKey` a `CustomUser`
- `videojuego` — `ForeignKey` a `Videojuego`
- `comentario`, `calificacion` (1 a 5), `fecha_creacion`
- Restricción `unique_together` — un usuario solo puede reseñar un juego una vez

### `Compra` — `store/models.py`
Registra las transacciones y funciona como la biblioteca personal de cada usuario.
- `usuario` — `ForeignKey` a `CustomUser`
- `videojuego` — `ForeignKey` a `Videojuego`
- `fecha_compra`

---

## Funcionalidades

### Usuarios
- Registro de cuenta nueva con avatar y fecha de nacimiento
- Login y logout desde templates
- Carga de saldo virtual desde `/accounts/cargar-saldo/`

### Catálogo y restricción de edad
- Listado de videojuegos con portada, precio y clasificación por edad
- Si el usuario autenticado es menor que la `edad_minima` del juego, el botón de acceso al detalle se deshabilita automáticamente
- Si intenta acceder forzando la URL directamente, la vista lo redirige con un mensaje de error

### Simulación de compra
La vista de compra valida en orden:
1. Que el usuario no tenga ya el juego en su biblioteca
2. Que el usuario cumpla la edad mínima requerida
3. Que el usuario tenga saldo suficiente

Si pasa todas las validaciones, descuenta el precio del saldo y registra la `Compra`.

### CRUD de Videojuegos (Moderadores)
| Operación | URL | Permiso requerido |
|---|---|---|
| Crear | `/videojuegos/crear/` | `store.add_videojuego` |
| Editar | `/videojuegos/<pk>/editar/` | `store.change_videojuego` |
| Eliminar | `/videojuegos/<pk>/eliminar/` | `store.delete_videojuego` |

Los moderadores ven los botones de edición y eliminación directamente en la página de detalle del juego.

### CRUD de Reseñas (Usuarios)
| Operación | URL | Restricción |
|---|---|---|
| Crear | `/videojuegos/<pk>/resenas/crear/` | Solo si compró el juego y aún no reseñó |
| Editar | `/resenas/<pk>/editar/` | Solo el autor |
| Eliminar | `/resenas/<pk>/eliminar/` | Solo el autor |

### Context Processor
`store.context_processors.categorias_context` inyecta la variable `global_categorias` en todos los templates, permitiendo que el navbar muestre dinámicamente el listado de géneros disponibles.

---

## Permisos y grupos

El sistema usa el sistema de permisos nativo de Django.

- Se debe crear el grupo **`Moderadores`** desde `/admin/` y asignarle los permisos `store.add_videojuego`, `store.change_videojuego` y `store.delete_videojuego`.
- Las vistas de creación, edición y eliminación de videojuegos están protegidas con `@permission_required`.
- Las vistas de reseñas están protegidas con `@login_required` más validación de autoría en el backend.
- La vista de detalle (lectura) es pública para usuarios no autenticados, pero con funcionalidad limitada.

---

## Instalación y configuración

### Requisitos previos
- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone git@github.com:gblengino/tp_evaluativo_django.git
cd tp_evaluativo_django

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Correr el servidor
python manage.py runserver
```

Luego abrir el navegador en `http://127.0.0.1:8000/`.

---

## Estructura del proyecto

```
tp_evaluativo_django/
├── config/                  # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
├── store/                   # App principal de la tienda
│   ├── models.py            # Desarrollador, Categoria, Videojuego, Resena, Compra
│   ├── views.py             # Catálogo, detalle, compra, CRUD videojuegos y reseñas
│   ├── forms.py             # VideojuegoForm, ResenaForm
│   ├── urls.py              # Rutas de la tienda
│   ├── admin.py             # Panel de administración
│   └── context_processors.py
├── users/                   # App de usuarios
│   ├── models.py            # CustomUser
│   ├── views.py             # Registro, carga de saldo
│   ├── forms.py             # CustomUserForm
│   └── admin.py             # CustomUserAdmin
├── templates/
│   ├── base.html            # Layout base con navbar y mensajes
│   ├── registration/        # Login y registro
│   ├── store/               # Catálogo, detalle, formularios de juegos y reseñas
│   └── users/               # Carga de saldo
├── media/                   # Archivos subidos (portadas, avatares)
├── requirements.txt
└── manage.py
```

---

## Panel de administración

Accesible en `/admin/` con un superusuario. Permite gestionar todos los modelos con:
- **Filtros laterales** por categoría, desarrollador, calificación y fecha
- **Búsqueda** por título, usuario, nombre
- **Ordenamiento** por columnas
- Gestión de usuarios, grupos y permisos

---

## Capturas

En la carpeta `capturas/` en la raíz del proyecto se encuentran capturas de pantalla de la aplicación en funcionamiento, mostrando las distintas funcionalidades implementadas.

---

## Integrantes del grupo

#### Benavidez, Tomás
#### Blengino, Giuliano
#### Cambria, Valentino
