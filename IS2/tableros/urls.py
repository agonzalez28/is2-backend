# tableros/urls.py

from django.urls import path
from .views import crear_tablero, obtener_tableros_por_usuario, obtener_tablero_por_id

urlpatterns = [
    path('tableros/crear/', crear_tablero, name='crear_tablero'),
    path('tableros/usuario/<str:cod_usuario>/', obtener_tableros_por_usuario, name='obtener_tableros_por_usuario'),
]

