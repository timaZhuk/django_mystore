# this file make Cart object globally available in our project
# got to settings.py and in TEMPLATES add 'store.context_processors.cart'
from .cart import Cart

def cart(request):
    return {'cart':Cart(request)}

