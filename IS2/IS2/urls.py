"""
URL configuration for IS2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import home  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('api/', include('usuarios.urls')), 
    path('api/workspace/', include('workspace.urls')),
    path('api/tableros/', include('tableros.urls')),
    path('api/tableros/listas/', include('lista_tableros.urls')),
    path('api/tableros/listas/tarjetas/', include('tarjeta.urls')),
    path('api/tableros/listas/tarjetas/tareas/', include('tareas.urls'))    
]
    