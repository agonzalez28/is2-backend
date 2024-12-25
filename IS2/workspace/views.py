# workspace/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import workspace
from usuarios.models import usuario
from datetime import date
from django.http import HttpResponse
import json

@csrf_exempt
def crear_workspace(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            nom_proyecto = data.get('nom_proyecto')
            descripcion = data.get('descripcion')
            estado = data.get('estado', 'Activo')  # Valor por defecto: 'Activo'
            cod_usuario = data.get('cod_usuario')
            cod_usuarios = data.get('cod_usuarios', [])  # Lista de códigos de usuarios a agregar

            print(f"Nombre del proyecto: {nom_proyecto}, Descripción: {descripcion}, Estado: {estado}, Código de usuario: {cod_usuario}") 
            
            # Validaciones básicas
            if not nom_proyecto or not descripcion or not cod_usuario:
                return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

            # Obtener el usuario creador
            usuario_obj = usuario.objects.get(cod_usuario=cod_usuario)

            # Crear el nuevo workspace
            nuevo_workspace = workspace.objects.create(
                nom_proyecto=nom_proyecto,
                descripcion=descripcion,
                estado=estado,
                usu_creador=usuario_obj,
                fec_creacion=date.today(),
                usu_modificacion=usuario_obj.nom_usuario  # Se guarda el nombre del usuario modificador
            )

            # Agregar los usuarios al workspace
            usuarios_agregados = []  # Lista para almacenar los usuarios agregados
            for cod_user in cod_usuarios:
                try:
                    user_obj = usuario.objects.get(cod_usuario=cod_user)
                    nuevo_workspace.usuarios.add(user_obj)  # Agregar usuario al workspace
                    usuarios_agregados.append(user_obj.nom_usuario)  # Añadir el nombre del usuario a la lista
                except usuario.DoesNotExist:
                    print(f"Usuario con código {cod_user} no encontrado y no se agregará.")

            return JsonResponse({
                'mensaje': 'Workspace creado correctamente', 'cod_espacio': nuevo_workspace.cod_espacio,
                'nom_proyecto': nuevo_workspace.nom_proyecto,
                'descripcion': nuevo_workspace.descripcion,
                'estado': nuevo_workspace.estado,
                'usuarios': usuarios_agregados 
                }, status=201)
                
        except usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)
        except ValidationError as ve:
            return JsonResponse({'error': str(ve)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_workspaces_por_usuario(request, cod_usuario):
    if request.method == 'GET':
        try:
            workspaces_list = workspace.objects.filter(usu_creador__cod_usuario=cod_usuario).values()
            return JsonResponse(list(workspaces_list), safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_workspace(request, cod_espacio):
    if request.method == 'DELETE':
        try:
            # obtener el workspace por su código
            workspace_obj = workspace.objects.get(cod_espacio=cod_espacio)
            workspace_obj.delete()  # Eliminar el workspace
            return JsonResponse({'mensaje': 'Workspace eliminado correctamente'}, status=204)
        except workspace.DoesNotExist:
            return JsonResponse({'error': 'Workspace no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def actualizar_workspace(request, cod_espacio):
    if request.method == "PUT":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos para actualizar:", data)

            # Validar si se recibe el cod_espacio 
            try:
                workspace_obj = workspace.objects.get(cod_espacio=cod_espacio)
            except workspace.DoesNotExist:
                return JsonResponse({"error": "Workspace no encontrado"}, status=404)

            # Validar que se ha enviado el nuevo nombre del proyecto
            nom_proyecto = data.get("nom_proyecto")
            if not nom_proyecto:
                return JsonResponse({"error": "El nombre del proyecto es obligatorio"}, status=400)

            # Actualizar campo de nombre del proyecto
            workspace_obj.nom_proyecto = nom_proyecto
            workspace_obj.save()

            return JsonResponse({
                "mensaje": "Workspace actualizado con exito",
                "cod_espacio": workspace_obj.cod_espacio,
                "nom_proyecto": workspace_obj.nom_proyecto
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

