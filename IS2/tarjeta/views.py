from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tarjeta
from lista_tableros.models import ListaTableros
import json

@csrf_exempt
def crear_tarjeta(request):
    if request.method == "POST":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            
            nom_tarjeta = data.get("nom_tarjeta")
            descripcion = data.get("descripcion", "")  # Asignar una cadena vacía si no se pasa una descripción
            estado = data.get("estado", "NEW")  # Estado por defecto
            usu_encargado = data.get("usu_encargado", None)
            fec_vencimiento = data.get("fec_vencimiento", None)
            cod_lista = data.get("cod_lista")  # Se espera el cod_lista del cliente

            # Validar los campos obligatorios
            if not nom_tarjeta or not cod_lista:
                return JsonResponse({"error": "El nombre de la tarjeta y el codigo de la lista son obligatorios"}, status=400)

            # Validar si el cod_lista existe en la base de datos
            try:
                lista_obj = ListaTableros.objects.get(cod_lista=cod_lista)
            except ListaTableros.DoesNotExist:
                return JsonResponse({"error": "Lista no encontrada"}, status=404)

            # Crear la nueva tarjeta
            nueva_tarjeta = Tarjeta.objects.create(
                nom_tarjeta=nom_tarjeta,
                descripcion=descripcion,
                estado=estado,
                usu_encargado=usu_encargado,
                fec_vencimiento=fec_vencimiento,
                cod_lista=lista_obj
            )

            # Responder con los datos de la nueva tarjeta
            return JsonResponse({
                "mensaje": "Tarjeta creada exitosamente",
                "cod_tarjeta": nueva_tarjeta.cod_tarjeta,
                "nom_tarjeta": nueva_tarjeta.nom_tarjeta,
                "cod_lista": lista_obj.cod_lista
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def actualizar_tarjeta(request, cod_tarjeta):
    if request.method == "PUT":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos para actualizar:", data)

            # Validar que el cod_tarjeta se pasa y existe
            try:
                tarjeta_obj = Tarjeta.objects.get(cod_tarjeta=cod_tarjeta)
            except Tarjeta.DoesNotExist:
                return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)

            # Obtener solo los campos a actualizar
            nom_tarjeta = data.get("nom_tarjeta", tarjeta_obj.nom_tarjeta)  # Si no se pasa, se mantiene el valor actual
            descripcion = data.get("descripcion", tarjeta_obj.descripcion)

            # Actualizar solo los campos permitidos
            tarjeta_obj.nom_tarjeta = nom_tarjeta
            tarjeta_obj.descripcion = descripcion

            tarjeta_obj.save()

            # Responder con la tarjeta actualizada
            return JsonResponse({
                "mensaje": "Tarjeta actualizada exitosamente",
                "cod_tarjeta": tarjeta_obj.cod_tarjeta,
                "nom_tarjeta": tarjeta_obj.nom_tarjeta,
                "descripcion": tarjeta_obj.descripcion,
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def obtener_tarjetas(request, cod_lista):
    if request.method == "GET":
        try:
            # Verificar si la lista existe
            try:
                lista_obj = ListaTableros.objects.get(cod_lista=cod_lista)
            except ListaTableros.DoesNotExist:
                return JsonResponse({"error": "Lista no encontrada"}, status=404)
            
            # Obtener todas las tarjetas asociadas a esta lista
            tarjetas = Tarjeta.objects.filter(cod_lista=lista_obj)

            # Construir la respuesta con las tarjetas
            tarjetas_data = [{
                "cod_tarjeta": tarjeta.cod_tarjeta,
                "nom_tarjeta": tarjeta.nom_tarjeta,
                "descripcion": tarjeta.descripcion,
                "estado": tarjeta.estado,
                "usu_encargado": tarjeta.usu_encargado,
                "fec_vencimiento": tarjeta.fec_vencimiento,
            } for tarjeta in tarjetas]

            return JsonResponse({"tarjetas": tarjetas_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)
