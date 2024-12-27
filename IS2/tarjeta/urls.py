# tarjetas/urls.py
from django.urls import path
from .views import crear_tarjeta, actualizar_tarjeta, obtener_tarjetas, tarjetas_por_usuario, tarjetas_por_estado, resumen_tarjetas, tarjetas_atrasadas
urlpatterns = [
    path('crear_tarjeta/', crear_tarjeta, name='crear_tarjeta'),
    path('actualizar_tarjeta/<int:cod_tarjeta>/', actualizar_tarjeta, name='actualizar_tarjeta'),
    path('obtener_tarjetas/<int:cod_lista>/', obtener_tarjetas, name='obtener_tarjetas'),
    path('por_usuario/<int:cod_tablero>/', tarjetas_por_usuario, name='tarjetas_por_usuario'),
    path('por_estado/<int:cod_tablero>/', tarjetas_por_estado, name='tarjetas_por_estado'),
    path('atrasadas/<int:cod_tablero>/', tarjetas_atrasadas, name='tarjetas_atrasadas'),
    path('resumen/<int:cod_tablero>/', resumen_tarjetas, name='resumen_tarjetas'),

]
