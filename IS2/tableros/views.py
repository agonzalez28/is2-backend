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
            cod_espacio = data.get('cod_espacio')  # Asegúrate de que este valor esté presente
            cod_usuario = data.get('cod_usuario')

            print(f"cod_espacio recibido: {cod_espacio}")
          
           # Validaciones básicas
            if not nom_tablero or not descripcion or not cod_espacio or not cod_usuario:
                return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

            # Obtener el usuario creador y el workspace relacionado
            usuario_obj = usuario.objects.get(cod_usuario=cod_usuario)
            espacio_obj = workspace.objects.get(cod_espacio=cod_espacio)  # Aquí es donde buscas el cod_espacio

            # Crear el nuevo tablero
            nuevo_tablero = tableros.objects.create(
                nom_tablero=nom_tablero,
                descripcion=descripcion,
                cod_espacio=espacio_obj,
                usu_creador=usuario_obj,
                fec_creacion=date.today()
            )

            return JsonResponse({
                'mensaje': 'Tablero creado correctamente',
                'cod_tablero': nuevo_tablero.cod_tablero
            }, status=201)

        except usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({'error': 'Workspace no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_tableros_por_workspace(request, cod_espacio):
    if request.method == 'GET':
        try:
            print(f"Consulta para cod_espacio: {cod_espacio}")
            tableros_list = tableros.objects.filter(cod_espacio__cod_espacio=cod_espacio).values()

             # Retorna una lista vacía si no hay resultados
            return JsonResponse(list(tableros_list), safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_tablero(request, cod_tablero):
    if request.method == 'DELETE':
        try:
            # Buscar el tablero por su ID
            tablero = tableros.objects.get(cod_tablero=cod_tablero)
            tablero.delete()  # Eliminar el tablero

            return JsonResponse({'mensaje': 'Tablero eliminado correctamente'}, status=204)  # 204 No Content
        except tableros.DoesNotExist:
            return JsonResponse({'error': 'Tablero no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
