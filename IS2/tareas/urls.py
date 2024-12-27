from django.urls import path
from . import views

urlpatterns = [
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('actualizar_tarea/<int:cod_tarea>/', views.actualizar_tarea, name='actualizar_tarea'),
    path('obtener_tarea/<int:cod_tarjeta>/', views.obtener_tarea, name='obtener_tarea'),
]
