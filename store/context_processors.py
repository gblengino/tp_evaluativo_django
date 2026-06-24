from .models import Categoria

def navbar_items(request):

    enlaces = [
        {
            'texto': 'Inicio',
            'url': 'index',
            'icono': 'home',
            'login_required': False
        },
        {
            'texto': 'Biblioteca',
            'url': 'biblioteca',
            'icono': 'gamepad-2',
            'login_required': True
        },
        {
            'texto': 'Historial',
            'url': 'historial_compras',
            'icono': 'history',
            'login_required': True
        },
    ]

    return {
        'GLOBAL_MENU_NAVBAR': enlaces
    }

def redes_sociales(request):

    redes = [
        {
            'plataforma': 'Twitch', 
            'url': 'https://twitch.tv', 
            'icono': 'fa-brands fa-twitch', 
            'color': 'hover:text-[#9146FF]'
        },
        {
            'plataforma': 'YouTube', 
            'url': 'https://youtube.com', 
            'icono': 'fa-brands fa-youtube', 
            'color': 'hover:text-[#FF0000]'
        },
        {
            'plataforma': 'Instagram', 
            'url': 'https://instagram.com', 
            'icono': 'fa-brands fa-instagram', 
            'color': 'hover:text-[#E1306C]'
        },
        {
            'plataforma': 'Facebook', 
            'url': 'https://facebook.com', 
            'icono': 'fa-brands fa-facebook', 
            'color': 'hover:text-[#1877F2]'
        },
        {
            'plataforma': 'X', 
            'url': 'https://x.com', 
            'icono': 'fa-brands fa-x-twitter',
            'color': 'hover:text-[#F5F5F5]'
        },
    ]
    
    return {
        'GLOBAL_REDES_SOCIALES': redes
    }