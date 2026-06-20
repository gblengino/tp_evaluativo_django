# Tareas Pendientes del Proyecto (GameStore)

Este archivo detalla lo que ya se implementó como base del backend y cuáles son las tareas que quedan por hacer para el resto del equipo.

---

## 1. Lo que ya está desarrollado y listo para usar

### Base de Datos y Modelos
* **`CustomUser`:** Cuenta con `username`, `email`, `password`, `fecha_nacimiento`, `saldo` y `avatar` (foto de perfil). Incluye el método `get_edad()` para calcular automáticamente la edad.
* **`Desarrollador`:** Representa los estudios creadores.
* **`Categoria`:** Representa los géneros de los videojuegos.
* **`Videojuego`:** Contiene los datos del juego (`precio`, `edad_minima`, `imagen_portada`, y relaciones con desarrollador y géneros).
* **`Resena`:** Permite registrar comentarios y calificaciones de usuarios.
* **`Compra`:** Registra qué videojuegos adquirió cada usuario (su biblioteca).

### Panel de Administración (`/admin/`)
* Todos los modelos están registrados en `store/admin.py`.
* Los modelos cuentan con filtros de búsqueda, filtros laterales y ordenamiento listos en el admin.

### Lógica de Negocio y Seguridad en el Backend
* **Carga de Saldo:** Se puede cargar dinero en `/accounts/cargar-saldo/` que se acredita al usuario.
* **Simulación de Compra:** Al hacer clic en "Comprar" se valida que el usuario no tenga ya el juego, que sea mayor de la edad mínima y que tenga saldo suficiente. Si pasa todo, se le resta la plata de su `saldo` y se crea un registro de `Compra` en su biblioteca.
* **Carga/Creación de Videojuegos (Moderadores):** ¡Implementado! La vista `videojuegos/crear/` ya está funcional y protegida con permisos en el backend. Un moderador autenticado con el permiso `store.add_videojuego` verá el enlace "Cargar Juego" en el navbar y podrá cargar nuevos títulos y portadas directamente desde el sitio web.
* **Restricción de Edad:** En el catálogo, si el usuario es menor de la edad mínima requerida por el juego, el botón de ingresar al detalle y compra se deshabilita automáticamente. Si intenta ingresar forzando la URL directamente en el navegador, la vista lo rebota y le muestra un mensaje de advertencia.
* **Context Processor:** El listado global de géneros se inyecta en todas las páginas mediante `global_categorias` (se puede ver en el navbar).

---

## 2. Lo que debe hacer el resto del equipo

### A. Diseñar y Estilizar (Frontend / Maquetación)
* **Estilo General:** El proyecto tiene Tailwind CSS cargado por CDN en `templates/base.html` y una estructura responsive. Falta definir una paleta de colores oscuros (Dark Mode) y darle estilo estético premium a las tarjetas de juegos, botones, y formularios.
* **Formularios con Tailwind:** Para dar estilo a los formularios Django (`form.as_p` o campos individuales), se debe usar `widget_tweaks` que ya está configurado. Ejemplo en templates:
  `{% render_field field class="bg-gray-800 text-white rounded p-2" %}`
* **Navbar Dinámico:** Estilizar la barra de navegación y hacer interactivo el desplegable de "Géneros" que usa la variable `global_categorias`.

### B. Implementar los CRUDs Restantes

#### 1. CRUD de Reseñas (Cualquier usuario logueado que posea el juego)
* **Crear Reseña:**
  * En la vista de detalle de juego (`store/views.py`), ya está listo el check `ya_comprado`.
  * Se debe crear un formulario `ResenaForm` en `store/forms.py`.
  * Crear la vista en `store/views.py` para procesar el envío del comentario y calificación (del 1 al 5) y guardarlo.
* **Editar y Eliminar Reseña:**
  * Crear las vistas para editar o borrar una reseña.
  * **Importante:** Validar en el backend que el usuario que intenta editar o borrar la reseña sea el mismo autor (`request.user == resena.usuario`).

#### 2. CRUD de Videojuegos (Moderadores de la plataforma)
* **Crear Videojuego:** ¡YA ESTÁ HECHO! La vista (`videojuego_crear`), el formulario (`VideojuegoForm`) y la plantilla (`store/videojuego_form.html`) están completamente funcionales. Solo falta que los maquetadores le agreguen estilos con Tailwind.
* **Editar y Eliminar Videojuegos:**
  * Implementar las vistas de edición y eliminación si se desea que los moderadores hagan estas acciones desde la web (en lugar de usar el panel de `/admin/`).
  * **Seguridad (Permisos):** Proteger estas vistas usando los decoradores `@permission_required('store.change_videojuego')` y `@permission_required('store.delete_videojuego')`.

### C. Configurar Grupos de Permisos en el Panel de Admin
* Iniciar sesión como superusuario en `/admin/`.
* Ir a **Grupos** y crear un grupo llamado `"Moderadores"`.
* En la lista de permisos, asignarle a este grupo el permiso:
  * `store | videojuego | Can add videojuego`
  * *(Opcional)* Si implementan edición y borrado web en el futuro: `Can change videojuego` y `Can delete videojuego`.
* Asignar a los usuarios del equipo que tengan rol de moderador dentro de ese grupo.
