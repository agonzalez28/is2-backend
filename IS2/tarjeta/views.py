from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tarjeta
from lista_tableros.models import ListaTableros
from datetime import date
from django.db.models import Count, Value


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
            estado = data.get("estado", "P")  # Estado por defecto
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
            
            # Comprobar la cantidad de tarjetas en la lista
            if lista_obj.cant_tarjetas >= 5:
                return JsonResponse({"error": "No se pueden agregar más de 5 tarjetas por lista"}, status=400)
            
            # Crear la nueva tarjeta
            nueva_tarjeta = Tarjeta.objects.create(
                nom_tarjeta=nom_tarjeta,
                descripcion=descripcion,
                estado=estado,
                usu_encargado=usu_encargado,
                fec_vencimiento=fec_vencimiento,
                cod_lista=lista_obj, 
                fec_creacion= date.today()
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
            nom_tarjeta = data.get("nom_tarjeta", tarjeta_obj.nom_tarjeta) 
            descripcion = data.get("descripcion", tarjeta_obj.descripcion)
            estado = data.get("estado", tarjeta_obj.estado)  # Si no se pasa, mantiene el estado actual
            usu_encargado = data.get("usu_encargado", tarjeta_obj.usu_encargado)
            fec_vencimiento = data.get("fec_vencimiento", tarjeta_obj.fec_vencimiento)

            # Actualizar solo los campos permitidos
            tarjeta_obj.nom_tarjeta = nom_tarjeta
            tarjeta_obj.descripcion = descripcion
            tarjeta_obj.fec_vencimiento = fec_vencimiento
            tarjeta_obj.estado = estado
            tarjeta_obj.usu_encargado = usu_encargado

            tarjeta_obj.save()

            # Responder con la tarjeta actualizada
            return JsonResponse({
                "mensaje": "Tarjeta actualizada exitosamente",
                "cod_tarjeta": tarjeta_obj.cod_tarjeta,
                "nom_tarjeta": tarjeta_obj.nom_tarjeta,
                "descripcion": tarjeta_obj.descripcion,
                "fec_vencimiento": tarjeta_obj.fec_vencimiento,
                "estado": tarjeta_obj.estado,
                "usu_encargado": tarjeta_obj.usu_encargado,
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
                "fec_creacion": tarjeta.fec_creacion,
            } for tarjeta in tarjetas]

            return JsonResponse({"tarjetas": tarjetas_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def mover_tarjeta(request, cod_tarjeta):
    if request.method == "PUT":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            nuevo_cod_lista = data.get("nuevo_cod_lista")

            # Validar que el cod_tarjeta y nuevo_cod_lista se pasan y existen
            try:
                tarjeta_obj = Tarjeta.objects.get(cod_tarjeta=cod_tarjeta)
            except Tarjeta.DoesNotExist:
                return JsonResponse({"error": "Tarjeta no encontrada"}, status=404)
            
            try:
                nueva_lista_obj = ListaTableros.objects.get(cod_lista=nuevo_cod_lista)
            except ListaTableros.DoesNotExist:
                return JsonResponse({"error": "Lista de destino no encontrada"}, status=404)

            # Actualizar el cod_lista de la tarjeta
            tarjeta_obj.cod_lista = nueva_lista_obj
            tarjeta_obj.save()

            return JsonResponse({
                "mensaje": "Tarjeta movida exitosamente",
                "cod_tarjeta": tarjeta_obj.cod_tarjeta,
                "nuevo_cod_lista": nuevo_cod_lista
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def tarjetas_por_usuario(request, cod_tablero):
    if request.method == "GET":
        try:
            # Filtrar tarjetas por el tablero específico
            tarjetas_por_usuario = (
                Tarjeta.objects.filter(cod_lista__cod_tablero=cod_tablero)
                .values('usu_encargado')
                .annotate(total=Count('cod_tarjeta'))
                .order_by('-total')
            )
            return JsonResponse({"tarjetas_por_usuario": list(tarjetas_por_usuario)}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def tarjetas_por_estado(request, cod_tablero):
    if request.method == "GET":
        try:
            # Filtrar tarjetas por el tablero específico
            tarjetas_por_estado = (
                Tarjeta.objects.filter(cod_lista__cod_tablero=cod_tablero)
                .values('estado')
                .annotate(total=Count('cod_tarjeta'))
                .order_by('estado')
            )
            return JsonResponse({"tarjetas_por_estado": list(tarjetas_por_estado)}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def resumen_tarjetas(request):
    if request.method == "GET":
        try:
            # Tarjetas por usuario
            tarjetas_por_usuario = (
                Tarjeta.objects.values('usu_encargado')
                .annotate(total=Count('cod_tarjeta'))
                .order_by('-total')
            )

            # Tarjetas por estado
            tarjetas_por_estado = (
                Tarjeta.objects.values('estado')
                .annotate(total=Count('cod_tarjeta'))
                .order_by('estado')
            )

            # Tarjetas atrasadas
            hoy = date.today()
            tarjetas_atrasadas = Tarjeta.objects.filter(fec_vencimiento__lt=hoy, estado='To Do').count()

            return JsonResponse({
                "tarjetas_por_usuario": list(tarjetas_por_usuario),
                "tarjetas_por_estado": list(tarjetas_por_estado),
                "tarjetas_atrasadas": tarjetas_atrasadas
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

from datetime import date

@csrf_exempt
def tarjetas_atrasadas(request, cod_tablero):
    if request.method == "GET":
        try:
            hoy = date.today()
            # Filtrar tarjetas por tablero y fecha vencida
            atrasadas = Tarjeta.objects.filter(
                cod_lista__cod_tablero=cod_tablero,
                fec_vencimiento__lt=hoy,
                estado='E'
            )
            return JsonResponse({"tarjetas_atrasadas": atrasadas.count()}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)