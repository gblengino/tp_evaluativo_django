from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserForm

def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('')
    else:
        form = CustomUserForm()
    
    return render(request, 'registration/register.html', {'form':form})