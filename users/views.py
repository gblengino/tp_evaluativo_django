from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation

from .forms import CustomUserForm

def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES) # Note request.FILES to support avatars
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()
    
    return render(request, 'registration/register.html', {'form':form})

@login_required
def cargar_saldo(request):
    if request.method == 'POST':
        monto_str = request.POST.get('monto')
        try:
            monto = Decimal(monto_str)
            if monto <= 0:
                messages.error(request, "El monto debe ser mayor a cero.")
            else:
                usuario = request.user
                usuario.saldo += monto
                usuario.save()
                messages.success(request, f"Se han cargado ${monto:.2f} a tu saldo. Saldo actual: ${usuario.saldo:.2f}.")
                return redirect('index')
        except (ValueError, TypeError, InvalidOperation):
            messages.error(request, "Por favor, ingresa un monto válido.")
            
    return render(request, 'users/cargar_saldo.html')