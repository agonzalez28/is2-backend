# tableros/urls.py

from django.urls import path
from .views import crear_tablero, obtener_tableros_por_workspace,  eliminar_tablero, agregar_lista,eliminar_lista

urlpatterns = [
    path('crear/', crear_tablero, name='crear_tablero'),
    path('tableros/<int:cod_espacio>/', obtener_tableros_por_workspace, name='obtener_tableros'),
    path('eliminar/<int:cod_tablero>/', eliminar_tablero, name='eliminar_tablero'),
    path('agregar_lista/', agregar_lista, name='agregar_lista'),
    path('agregar_lista/<int:cod_lista>/', eliminar_lista, name='eliminar_lista'),
    
]

