# usuarios/urls.py
from django.urls import path
from .views import registro_usuario, login_usuario  # Importar la función correctamente

urlpatterns = [
    path('registrar/', registro_usuario, name='registro_usuario'),
    path('login/', login_usuario, name='login_usuario'),
]
