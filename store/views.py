from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Videojuego, Compra, Resena
from .forms import VideojuegoForm, ResenaForm

def index(request):
    videojuegos = Videojuego.objects.all()
    edad_usuario = 0
    if request.user.is_authenticated:
        edad_usuario = request.user.get_edad()
    
    contexto = {
        'videojuegos': videojuegos,
        'edad_usuario': edad_usuario,
    }
    return render(request, 'store/index.html', contexto)

def videojuego_detalle(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    
    # Verificación de edad en backend
    if request.user.is_authenticated and not request.user.is_staff:
        if request.user.get_edad() < videojuego.edad_minima:
            messages.error(request, f"No tienes edad suficiente para ver los detalles de {videojuego.titulo}.")
            return redirect('index')
    
    ya_comprado = False
    ya_resenado = False
    resena_propia = None
    if request.user.is_authenticated:
        ya_comprado = Compra.objects.filter(usuario=request.user, videojuego=videojuego).exists()
        resena_propia = Resena.objects.filter(usuario=request.user, videojuego=videojuego).first()
        ya_resenado = resena_propia is not None

    reseñas = videojuego.resena_set.all()

    contexto = {
        'videojuego': videojuego,
        'ya_comprado': ya_comprado,
        'ya_resenado': ya_resenado,
        'resena_propia': resena_propia,
        'reseñas': reseñas,
    }
    return render(request, 'store/detalle.html', contexto)

@login_required
def comprar_videojuego(request, pk):
    if request.method == 'POST':
        videojuego = get_object_or_404(Videojuego, pk=pk)
        usuario = request.user
        
        # 1. Validar que no lo tenga ya comprado
        if Compra.objects.filter(usuario=usuario, videojuego=videojuego).exists():
            messages.warning(request, f"Ya tienes {videojuego.titulo} en tu biblioteca.")
            return redirect('videojuego_detalle', pk=pk)
        
        # 2. Validar restricción de edad
        if usuario.get_edad() < videojuego.edad_minima:
            messages.error(request, f"No cumples con la edad mínima requerida para comprar {videojuego.titulo}.")
            return redirect('index')
        
        # 3. Validar saldo
        if usuario.saldo < videojuego.precio:
            messages.error(request, f"No tienes saldo suficiente para comprar {videojuego.titulo}. Tu saldo actual es ${usuario.saldo}.")
            return redirect('videojuego_detalle', pk=pk)
        
        # Descontar saldo y guardar compra
        usuario.saldo -= videojuego.precio
        usuario.save()
        
        Compra.objects.create(usuario=usuario, videojuego=videojuego)
        messages.success(request, f"¡Compraste {videojuego.titulo} con éxito!")
        return redirect('videojuego_detalle', pk=pk)
        
    return redirect('index')

@permission_required('store.add_videojuego', raise_exception=True)
def videojuego_crear(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Videojuego creado con éxito en el catálogo!")
            return redirect('index')
    else:
        form = VideojuegoForm()

    return render(request, 'store/videojuego_form.html', {'form': form})


@permission_required('store.change_videojuego', raise_exception=True)
def videojuego_editar(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=videojuego)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡{videojuego.titulo} actualizado con éxito!")
            return redirect('videojuego_detalle', pk=pk)
    else:
        form = VideojuegoForm(instance=videojuego)

    return render(request, 'store/videojuego_form.html', {'form': form, 'editando': True, 'videojuego': videojuego})


@permission_required('store.delete_videojuego', raise_exception=True)
def videojuego_eliminar(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        titulo = videojuego.titulo
        videojuego.delete()
        messages.success(request, f"¡{titulo} eliminado del catálogo.")
        return redirect('index')

    return render(request, 'store/videojuego_confirm_delete.html', {'videojuego': videojuego})


@login_required
def resena_crear(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)

    if not Compra.objects.filter(usuario=request.user, videojuego=videojuego).exists():
        messages.error(request, "Solo puedes reseñar juegos que hayas comprado.")
        return redirect('videojuego_detalle', pk=pk)

    if Resena.objects.filter(usuario=request.user, videojuego=videojuego).exists():
        messages.warning(request, "Ya escribiste una reseña para este juego.")
        return redirect('videojuego_detalle', pk=pk)

    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            resena.videojuego = videojuego
            resena.save()
            messages.success(request, "¡Reseña publicada con éxito!")
            return redirect('videojuego_detalle', pk=pk)
    else:
        form = ResenaForm()

    return render(request, 'store/resena_form.html', {'form': form, 'videojuego': videojuego})


@login_required
def resena_editar(request, pk):
    resena = get_object_or_404(Resena, pk=pk)

    if resena.usuario != request.user:
        messages.error(request, "No tienes permiso para editar esta reseña.")
        return redirect('videojuego_detalle', pk=resena.videojuego.pk)

    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            messages.success(request, "Reseña actualizada con éxito.")
            return redirect('videojuego_detalle', pk=resena.videojuego.pk)
    else:
        form = ResenaForm(instance=resena)

    return render(request, 'store/resena_form.html', {'form': form, 'videojuego': resena.videojuego, 'editando': True})


@login_required
def resena_eliminar(request, pk):
    resena = get_object_or_404(Resena, pk=pk)

    if resena.usuario != request.user:
        messages.error(request, "No tienes permiso para eliminar esta reseña.")
        return redirect('videojuego_detalle', pk=resena.videojuego.pk)

    videojuego_pk = resena.videojuego.pk
    if request.method == 'POST':
        resena.delete()
        messages.success(request, "Reseña eliminada.")
        return redirect('videojuego_detalle', pk=videojuego_pk)

    return render(request, 'store/resena_confirm_delete.html', {'resena': resena})

@login_required
def biblioteca(request):
    biblioteca = Videojuego.objects.filter(compra__usuario=request.user).distinct()

    return render(request, 'store/biblioteca.html', {'biblioteca': biblioteca})

@login_required
def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user).select_related('videojuego').order_by('-fecha_compra')

    return render(request, 'store/historial.html', {'historial_compras': compras})