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
            estado = data.get('estado', 'Publico')  # Valor por defecto: 'Publico'
            cod_usuario = data.get('cod_usuario')
        
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

            return JsonResponse({'mensaje': 'Workspace creado correctamente', 'cod_espacio': nuevo_workspace.cod_espacio}, status=201)
        
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