# usuarios/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from .models import usuario
from django.contrib.auth.hashers import make_password, check_password

from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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

@csrf_exempt
def obtener_usuarios(request):
    if request.method == 'GET':
        try:
            usuarios_list = usuario.objects.values('cod_usuario', 'nom_usuario')  # Solo devuelve el código y el nombre
            return JsonResponse(list(usuarios_list), safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validar el token con Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "803348551466-oboa8q0363scjbhe6rp16nakdo999mar.apps.googleusercontent.com")
            email = idinfo.get('email')
            name = idinfo.get('name')

            # Busca o crea al usuario en la base de datos
            user, created = User.objects.get_or_create(email=email, defaults={'username': name})

            # Genera un JWT para el usuario
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login exitoso',
                'authToken': str(refresh.access_token),  # Token de acceso
                'refreshToken': str(refresh),  # Token de refresco
                'user': {'email': user.email, 'name': user.username}
            })
        except ValueError as e:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)