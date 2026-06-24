from django import forms
from .models import Videojuego

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'precio', 'edad_minima', 'imagen_portada', 'desarrollador', 'categorias']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':5, 'cols':40}),
            'precio': forms.NumberInput(attrs={'step':'0.01'}),
            'categorias': forms.CheckboxSelectMultiple(),
        }
