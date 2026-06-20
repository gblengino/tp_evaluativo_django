from django import forms
from .models import Videojuego

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'precio', 'edad_minima', 'imagen_portada', 'desarrollador', 'categorias']
        widgets = {
            'categorias': forms.CheckboxSelectMultiple(),
        }
