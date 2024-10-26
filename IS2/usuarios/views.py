# usuarios/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from .models import usuario
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt  # Solo para evitar problemas de CSRF en este ejemplo (mejor agregar CSRF Token en producción)
def registro_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Aquí se usa JSON
        nom_usuario = data.get('username')  # Corregir los nombres según tu front
        nombre = data.get('name')
        dir_correo = data.get('email')  # Corregir los nombres según tu front
        pass_usuario = make_password(data.get('password'))# Hashear la contraseña
        # Verificar si el correo o nombre de usuario ya existen
        if usuario.objects.filter(nom_usuario=nom_usuario).exists():
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)

        if usuario.objects.filter(dir_correo=dir_correo).exists():
            return JsonResponse({'error': 'El correo ya está en uso'}, status=400)
        
        # Crear el usuario en la tabla personalizada
        nuevo_usuario = usuario.objects.create(
            nombre = nombre,
            nom_usuario=nom_usuario,
            dir_correo=dir_correo,
            pass_usuario=pass_usuario
        )   
        return JsonResponse({'mensaje': 'Usuario creado correctamente'}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def login_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom_usuario = data.get('username')
            pass_usuario = data.get('password')

            # Buscar el usuario en la base de datos
            try:
                user = usuario.objects.get(nom_usuario=nom_usuario)
                if check_password(pass_usuario, user.pass_usuario):  # Verificar contraseña
                    return JsonResponse({
                        'mensaje': 'Login exitoso',
                        'cod_usuario': user.cod_usuario,  # Devolver el cod_usuario
                        'nombre': user.nombre
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Contraseña incorrecta'}, status=400)
            except usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def home(request):
    return HttpResponse("¡Bienvenido a la aplicación de gestión de tareas!")
