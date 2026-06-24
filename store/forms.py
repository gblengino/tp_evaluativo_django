from django import forms
from django.core.exceptions import ValidationError
from .models import Videojuego, Resena

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'precio', 'edad_minima', 'imagen_portada', 'desarrollador', 'categorias']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':5, 'cols':40}),
            'precio': forms.NumberInput(attrs={'step':'0.01'}),
            'categorias': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['imagen_portada'].required = False

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['comentario', 'calificacion']

    def clean_calificacion(self):
        valor = self.cleaned_data.get('calificacion')
        if valor is None or not (1 <= valor <= 5):
            raise ValidationError("La calificación debe ser un número entre 1 y 5.")
        return valor
