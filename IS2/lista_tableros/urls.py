# listas_tableros/urls.py

from django.urls import path
from .views import agregar_lista, eliminar_lista, obtener_listas_tableros

urlpatterns = [
    path('agregar_lista/', agregar_lista, name='agregar_lista'),
    path('eliminar_lista/<int:cod_lista>/', eliminar_lista, name='eliminar_lista'),
    path('obtener_listas_tableros/<int:cod_tablero>/',obtener_listas_tableros, name='obtener_listas'),
]

