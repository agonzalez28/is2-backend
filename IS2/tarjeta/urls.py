# tarjetas/urls.py
from django.urls import path
from .views import crear_tarjeta, actualizar_tarjeta, obtener_tarjetas

urlpatterns = [
    path('crear_tarjeta/', crear_tarjeta, name='crear_tarjeta'),
    path('actualizar_tarjeta/<int:cod_tarjeta>/', actualizar_tarjeta, name='actualizar_tarjeta'),
    path('obtener_tarjetas/<int:cod_lista>/', obtener_tarjetas, name='obtener_tarjetas'), 
]
