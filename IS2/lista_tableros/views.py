# lista_tableros/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ListaTableros
from tableros.models import tableros  # Importamos el modelo de tableros
import json

@csrf_exempt
def agregar_lista(request):
    if request.method == "POST":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            nom_lista = data.get("nom_lista")
            cant_tarjetas = data.get("cant_tarjetas")
            cod_tablero = data.get("cod_tablero")

            print(f"cod_tablero recibido: {cod_tablero}")

            # Validación de datos
            if not nom_lista or not cod_tablero:
                return JsonResponse({"error": "El nombre de la lista y el código del tablero son obligatorios"}, status=400)

            # Obtener el objeto del tablero al que pertenece la lista y crear la nueva lista de tableros
            tablero_obj = tableros.objects.get(cod_tablero=cod_tablero)

            nueva_lista = ListaTableros.objects.create(
                nom_lista=nom_lista,
                cant_tarjetas=cant_tarjetas,
                cod_tablero=tablero_obj  
            )

            # Responder con éxito, incluyendo el id de la lista y el cod_tablero
            return JsonResponse({
                "mensaje": "Lista agregada exitosamente",
                "cod_lista": nueva_lista.cod_lista,
                "cod_tablero": tablero_obj.cod_tablero
            }, status=201)

        except tableros.DoesNotExist:
            return JsonResponse({"error": "Tablero no encontrado"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def eliminar_lista(request, cod_lista):
    if request.method == 'DELETE':
        try:
            # Buscar la lista por su ID
            lista = ListaTableros.objects.get(cod_lista=cod_lista)
            lista.delete()  # Eliminar la lista
            return JsonResponse({'mensaje': 'Lista eliminada correctamente'}, status=204)  # 204 No Content
        except ListaTableros.DoesNotExist:
            return JsonResponse({'error': 'Lista no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_listas_tableros(request, cod_tablero):
    if request.method == 'GET':
        try:
            # Filtrar por código de tablero
            listas = ListaTableros.objects.filter(cod_tablero__cod_tablero=cod_tablero)

            # Crear una lista con los datos serializados
            listas_data = [
                {
                    "cod_lista": lista.cod_lista,
                    "nom_lista": lista.nom_lista,
                    "cant_tarjetas": lista.cant_tarjetas,
                    "cod_tablero": lista.cod_tablero.cod_tablero,
                }
                for lista in listas
            ]
            return JsonResponse({"listas": listas_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
