# tableros/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import tableros
from usuarios.models import usuario
from workspace.models import workspace
from datetime import date
from django.http import HttpResponse
import json

@csrf_exempt
def crear_tablero(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            nom_tablero = data.get('nom_tablero')
            descripcion = data.get('descripcion')
            cod_espacio = data.get('cod_espacio')  # cod_espacio del workspace relacionado
            cod_usuario = data.get('cod_usuario')  # cod_usuario del usuario creador
            
            print(f"Nombre del tablero: {nom_tablero}, Descripción: {descripcion}, Código de espacio: {cod_espacio}, Código de usuario: {cod_usuario}")  
            
            # Validaciones básicas
            if not nom_tablero or not descripcion or not cod_espacio or not cod_usuario:
                return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

            # Obtener el usuario creador relacionado
            usuario_obj = usuario.objects.get(cod_usuario=cod_usuario)

            # Obtener el workspace relacionado
            espacio_obj = workspace.objects.get(cod_espacio=cod_espacio)

            # Crear el nuevo tablero
            nuevo_tablero = Tablero.objects.create(
                nom_tablero=nom_tablero,
                descripcion=descripcion,
                cod_espacio=espacio_obj,
                usu_creador=usuario_obj,
                fec_creacion=date.today()
            )

            return JsonResponse({'mensaje': 'Tablero creado correctamente', 'cod_tablero': nuevo_tablero.cod_tablero}, status=201)
        
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Workspace.DoesNotExist:
            return JsonResponse({'error': 'Workspace no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_tableros_por_usuario(request, cod_usuario):
    if request.method == 'GET':
        try:
            tableros_list = Tablero.objects.filter(usu_creador__cod_usuario=cod_usuario).values()
            return JsonResponse(list(tableros_list), safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_tablero_por_id(request, cod_tablero):
    if request.method == 'GET':
        try:
            tablero = Tablero.objects.get(cod_tablero=cod_tablero)
            return JsonResponse({
                'cod_tablero': tablero.cod_tablero,
                'nom_tablero': tablero.nom_tablero,
                'descripcion': tablero.descripcion,
                'cod_espacio': tablero.cod_espacio.cod_espacio,
                'usu_creador': tablero.usu_creador.cod_usuario,
                'fec_creacion': tablero.fec_creacion,
            }, status=200)
        except Tablero.DoesNotExist:
            return JsonResponse({'error': 'Tablero no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

