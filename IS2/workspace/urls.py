# workspace/urls.py

from django.urls import path
from .views import crear_workspace, obtener_workspaces_por_usuario, eliminar_workspace

urlpatterns = [
    path('crear/', crear_workspace, name='crear_workspace'),
    path('workspaces/<str:cod_usuario>/', obtener_workspaces_por_usuario, name='obtener_workspaces_por_usuario'),
     path('eliminar/<int:cod_espacio>/', eliminar_workspace, name='eliminar_workspace'),   
]
