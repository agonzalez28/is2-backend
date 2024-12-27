from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tarea
from tarjeta.models import Tarjeta
from datetime import date
import json

@csrf_exempt
def crear_tarea(request):
    if request.method == "POST":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            
            descripcion = data.get("descripcion", "")
            estado = data.get("estado", "NEW")
            fec_vencimiento = data.get("fec_vencimiento")
            cod_tarjeta = data.get("cod_tarjeta") 

            print("cod_tarjeta",  cod_tarjeta )

            # Validar si el cod_tarjeta existe en la base de datos
            try:
                tarjeta_obj = Tarjeta.objects.get(cod_tarjeta=cod_tarjeta)
            except Tarjeta.DoesNotExist:
                return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)

            # Crear la nueva tarea
            nueva_tarea = Tarea.objects.create(
                descripcion=descripcion,
                estado=estado,
                cod_tarjeta=tarjeta_obj,
                fec_creacion=date.today(),
                fec_vencimiento=fec_vencimiento
            )

            # Responder con exito incluyendo los datos de la nueva tarea
            return JsonResponse({
                "mensaje": "Tarea creada exitosamente",
                "cod_tarea": nueva_tarea.cod_tarea,
                "cod_tarjeta": tarjeta_obj.cod_tarjeta
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def actualizar_tarea(request, cod_tarea):
    if request.method == "PUT":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos para actualizar:", data)

            # Validar que el cod_tarea se pasa y existe
            try:
                tarea_obj = Tarea.objects.get(cod_tarea=cod_tarea)
            except Tarea.DoesNotExist:
                return JsonResponse({"error": "Tarea no encontrada"}, status=404)

            # Obtener solo los campos a actualizar
            descripcion = data.get("descripcion", tarea_obj.descripcion)
            estado = data.get("estado", tarea_obj.estado)
            fec_vencimiento = data.get("fec_vencimiento", tarea_obj.fec_vencimiento)

            # Actualizar solo los campos permitidos
            tarea_obj.descripcion = descripcion
            tarea_obj.estado = estado
            tarea_obj.fec_vencimiento = fec_vencimiento

            tarea_obj.save()

            # Responder con la tarea actualizada
            return JsonResponse({
                "mensaje": "Tarea actualizada exitosamente",
                "cod_tarea": tarea_obj.cod_tarea,
                "descripcion": tarea_obj.descripcion,
                "estado": tarea_obj.estado,
                "fec_vencimiento": tarea_obj.fec_vencimiento
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def obtener_tarea(request, cod_tarjeta):
    if request.method == "GET":
        try:
            # Verificar si la tarjeta existe
            try:
                tarjeta_obj = Tarjeta.objects.get(cod_tarjeta=cod_tarjeta)
            except Tarjeta.DoesNotExist:
                return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)

            # Obtener todas las tareas asociadas a esta tarjeta
            tareas = Tarea.objects.filter(cod_tarjeta=tarjeta_obj)

            # Construir la respuesta con las tareas
            tareas_data = [{
                "cod_tarea": tarea.cod_tarea,
                "descripcion": tarea.descripcion,
                "estado": tarea.estado,
                "fec_vencimiento": tarea.fec_vencimiento,
            } for tarea in tareas]

            return JsonResponse({"tareas": tareas_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

