# usuarios/urls.py
from django.urls import path
from .views import registro_usuario, login_usuario, obtener_usuarios  # Importar la función correctamente

urlpatterns = [
    path('registrar/', registro_usuario, name='registro_usuario'),
    path('login/', login_usuario, name='login_usuario'),
    path('usuarios/', obtener_usuarios, name='obtener_usuarios')
]
