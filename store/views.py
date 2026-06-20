from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Videojuego, Compra
from .forms import VideojuegoForm

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
    if request.user.is_authenticated:
        if request.user.get_edad() < videojuego.edad_minima:
            messages.error(request, f"No tienes edad suficiente para ver los detalles de {videojuego.titulo}.")
            return redirect('index')
    
    ya_comprado = False
    if request.user.is_authenticated:
        ya_comprado = Compra.objects.filter(usuario=request.user, videojuego=videojuego).exists()
    
    reseñas = videojuego.resena_set.all()
    
    contexto = {
        'videojuego': videojuego,
        'ya_comprado': ya_comprado,
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