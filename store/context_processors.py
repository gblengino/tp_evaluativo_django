from .models import Categoria

def categorias_context(request):
    return {
        'global_categorias': Categoria.objects.all()
    }
